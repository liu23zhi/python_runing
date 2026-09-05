const RUNTIME_NAMESPACE = '__MAP_KEY_RUNTIME__'

let runtimeLoadPromise = null

function loadRuntimeScript(scriptUrl) {
  if (runtimeLoadPromise) return runtimeLoadPromise
  runtimeLoadPromise = new Promise((resolve, reject) => {
    const existing = document.querySelector('script[data-map-key-runtime="1"]')
    if (existing) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = scriptUrl || '/scripts/map_key_runtime.js'
    script.async = true
    script.dataset.mapKeyRuntime = '1'
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('地图密钥运行时脚本加载失败'))
    document.head.appendChild(script)
  })
  return runtimeLoadPromise
}

export async function hydrateMapProviderSecrets(initialData) {
  if (!initialData || typeof initialData !== 'object') return initialData
  const keyBundle = initialData.map_provider_key_bundle
  if (!keyBundle || typeof keyBundle !== 'object') return initialData
  if (keyBundle.available === false) return initialData

  await loadRuntimeScript(keyBundle.runtime_script)
  const runtime = window[RUNTIME_NAMESPACE]
  if (!runtime || typeof runtime.decryptMapProviderKeys !== 'function') {
    throw new Error('地图密钥运行时不可用')
  }

  const decryptedProviders = await runtime.decryptMapProviderKeys(keyBundle)
  const nextProviders = { ...(initialData.map_providers || {}) }
  Object.entries(decryptedProviders || {}).forEach(([provider, secrets]) => {
    const current = nextProviders[provider]
    nextProviders[provider] = {
      ...(current && typeof current === 'object' ? current : {}),
      ...(secrets && typeof secrets === 'object' ? secrets : {}),
    }
  })

  return {
    ...initialData,
    map_providers: nextProviders,
  }
}
