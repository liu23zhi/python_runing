/* map key runtime template: server will inject private key and obfuscate this script in memory */
(function (globalScope) {
  "use strict";

  const runtimePrivateKeyPem = __MAP_KEY_RUNTIME_PRIVATE_KEY_PEM__;
  const runtimeVersion = __MAP_KEY_RUNTIME_VERSION__;
  const runtimeNamespace = "__MAP_KEY_RUNTIME_NAMESPACE__";
  let runtimePrivateCryptoKeyPromise = null;

  function base64ToBytes(base64Text) {
    const binaryText = atob(base64Text);
    const bytes = new Uint8Array(binaryText.length);
    for (let i = 0; i < binaryText.length; i += 1) {
      bytes[i] = binaryText.charCodeAt(i);
    }
    return bytes;
  }

  function pemToArrayBuffer(pemText) {
    const sanitized = String(pemText || "").replace(/-----[^-]+-----/g, "").replace(/\s+/g, "");
    return base64ToBytes(sanitized).buffer;
  }

  async function getRuntimePrivateKey() {
    if (runtimePrivateCryptoKeyPromise) return runtimePrivateCryptoKeyPromise;
    runtimePrivateCryptoKeyPromise = crypto.subtle.importKey(
      "pkcs8",
      pemToArrayBuffer(runtimePrivateKeyPem),
      { name: "RSA-OAEP", hash: "SHA-256" },
      false,
      ["decrypt"]
    );
    return runtimePrivateCryptoKeyPromise;
  }

  async function decryptSingleCiphertext(base64Ciphertext, privateKey) {
    if (!base64Ciphertext) return "";
    const encryptedBuffer = base64ToBytes(base64Ciphertext);
    const plainBuffer = await crypto.subtle.decrypt(
      { name: "RSA-OAEP" },
      privateKey,
      encryptedBuffer
    );
    return new TextDecoder().decode(plainBuffer);
  }

  async function decryptMapProviderKeys(bundle) {
    const providersPayload = (bundle && bundle.providers && typeof bundle.providers === "object")
      ? bundle.providers
      : {};
    const privateKey = await getRuntimePrivateKey();
    const providers = {};
    for (const [providerName, secretInfo] of Object.entries(providersPayload)) {
      const fieldName = secretInfo && secretInfo.field ? String(secretInfo.field) : "";
      if (!fieldName) continue;
      const decrypted = await decryptSingleCiphertext(secretInfo.ciphertext || "", privateKey);
      if (!providers[providerName]) providers[providerName] = {};
      providers[providerName][fieldName] = decrypted;
    }
    return providers;
  }

  globalScope[runtimeNamespace] = Object.freeze({
    version: runtimeVersion,
    decryptMapProviderKeys,
  });
})(window);
