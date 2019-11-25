import io

import qrcode


class QRHandler:

    @staticmethod
    def create_qr_image(user_id, otp):
        qr_object = {
            'user_id': user_id,
            'otp': otp
        }
        img = qrcode.make(qr_object)
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        return buffer.getvalue()
