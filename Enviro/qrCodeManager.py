from django.conf import settings
from Enviro.models import Booth
from qrcode import QRCode, constants

class QRCodeManager(object):

    PORT = ":9999"

    @staticmethod
    def generate_qr_code(booth = None):

        if booth is None:
            data_url = "/checkout"
            img_seed_name = "checkout"
        else:
            data_url = "/checkin/" + str(booth.id)
            img_seed_name = "boothId=" + str(booth.id) + "_boothName=" + str(booth.title)

        return QRCodeManager._gen_code_img(data_url, img_seed_name)



    @staticmethod
    def _gen_code_img(data_url, img_seed_name):

        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        full_url = QRCodeManager.PORT + data_url
        qr.add_data(full_url)
        qr.make(fit=True)
        img = qr.make_image()

        img_name = "qrcode_" + img_seed_name + ".png"
        img_path = settings.MEDIA_ROOT + "qrcodes\\" + img_name
        img_url = settings.MEDIA_URL + "qrcodes\\" + img_name

        img.save(img_path, 'PNG')

        return img_url
