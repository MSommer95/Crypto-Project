import io

import qrcode


class QRHandler:

    @staticmethod
    def create_qr_image(otp):
        img = qrcode.make(otp)
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        return buffer.getvalue()
