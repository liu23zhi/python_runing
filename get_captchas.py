import random
import string

class MicroPixelCaptcha:
    # 5x7 字库 (保持不变)
    FONT = {
        'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
        'C': ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
        'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
        'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
        'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
        'G': ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
        'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
        'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
        'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
        'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
        'M': ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
        'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
        'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
        'Q': ["01110", "10001", "10001", "10001", "10101", "10011", "01101"],
        'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
        'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
        'W': ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
        'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
        'Y': ["10001", "10001", "10001", "01010", "00100", "00100", "00100"],
        'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
        '0': ["01110", "10011", "10101", "10101", "10101", "11001", "01110"],
        '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
        '2': ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
        '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
        '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
        '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
        '6': ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
        '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
        '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
        '9': ["01110", "10001", "10001", "01111", "00001", "00001", "01110"]
    }

    def _random_string(self, length: int) -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def generate(self, length: int = 4, scale_factor: int = 2, noise_level: float = 0.08):
        """
        生成高密度微像素验证码
        :param length: 验证码字符数
        :param scale_factor: 细分倍数 (建议2或3)
        :param noise_level: 噪点比例
        """
        code = ''.join(random.choices(list(self.FONT.keys()), k=length))

        # 1. 构建基础逻辑行
        char_patterns = [self.FONT.get(c, ["11111"] * 7) for c in code]
        base_rows = ['0'.join(row_tuple) for row_tuple in zip(*char_patterns)]
        
        # 2. 像素细分与扩展
        expanded_bit_string = []
        for row in base_rows:
            # 水平扩展
            expanded_row_str = "".join([bit * scale_factor for bit in row])
            # 垂直扩展
            for _ in range(scale_factor):
                expanded_bit_string.append(expanded_row_str)
        
        full_bit_stream = "".join(expanded_bit_string)

        # 3. 计算 Grid 布局参数
        logic_width = length * 5 + (length - 1)
        grid_cols = logic_width * scale_factor

        # 4. 生成 HTML 像素块
        cls_con = self._random_string(10)
        cls_bg = self._random_string(5)
        cls_fg = self._random_string(5)
        
        pixels = []
        for bit in full_bit_stream:
            is_fg = (bit == '1')
            if random.random() < noise_level:
                is_fg = not is_fg
            
            pixels.append(f'<i class="{cls_fg if is_fg else cls_bg}"></i>')

        html_content = ''.join(pixels)

        # 5. CSS 样式优化 (黑白风格)
        pixel_size = 12 // scale_factor
        if pixel_size < 4: pixel_size = 4
        
        css = f"""<style>
.{cls_con}{{
    display:grid;
    grid-template-columns:repeat({grid_cols}, {pixel_size}px);
    gap:1px;
    background:#000;
    padding:10px;
    width:fit-content;
    border:1px solid #333;
}}
.{cls_con} i{{
    width:{pixel_size}px;
    height:{pixel_size}px;
    display:block;
    border-radius:0;
}}
.{cls_bg}{{background:#000;}}
.{cls_fg}{{background:#fff;}}
</style>"""

        full_html = f'<div class="{cls_con}">{html_content}</div>{css}'
        return code, full_html

if __name__ == "__main__":

    gen = MicroPixelCaptcha()
    code, html = gen.generate(length=4, scale_factor=4, noise_level=0.2)
    # 字数、细分倍数、噪点比例
    print(f"Code: {code}")
    print(html)