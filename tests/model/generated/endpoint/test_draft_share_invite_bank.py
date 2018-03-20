from datetime import datetime
from datetime import timedelta

from bunq.sdk.context import BunqContext
from bunq.sdk.model.generated.endpoint import DraftShareInviteBank
from bunq.sdk.model.generated.endpoint import DraftShareInviteBankQrCodeContent
from bunq.sdk.model.generated.object_ import DraftShareInviteEntry
from bunq.sdk.model.generated.object_ import ShareDetail
from bunq.sdk.model.generated.object_ import ShareDetailReadOnly
from tests.bunq_test import BunqSdkTestCase
from tests.config import Config


class TestDraftShareInvite(BunqSdkTestCase):
    """
    Tests:
        DraftShareInviteBankEntry
        DraftShareInviteBankQrCodeContent
    """

    @classmethod
    def setUpClass(cls):
        cls._OUT_PUT_FILE_PATH = 'connectQr.png'
        cls._WRITE_BYTES = 'wb'
        cls._EXPIRATION_ADDED_TIME = 1
        cls._USER_ID = Config.get_user_id()
        BunqContext.load_api_context(cls._get_api_context())

    def test_draft_share_invite_bank(self):
        """
        Tests the creation of a connect and retrieves the QR code bound to
        this connect.

        This test has no assertion as of its testing to see if the code runs
        without errors
        """

        share_detail = ShareDetail(
            read_only=ShareDetailReadOnly(True, True, True)
        )
        share_settings = DraftShareInviteEntry(share_detail)

        draft_id = DraftShareInviteBank.create(self.expiration_date,
                                               share_settings).value

        connect_qr = DraftShareInviteBankQrCodeContent.list(draft_id).value

        with open(self._OUT_PUT_FILE_PATH, self._WRITE_BYTES) as f:
            f.write(connect_qr)

    @property
    def expiration_date(self):
        """
        :rtype: str
        """

        date = datetime.utcnow() + timedelta(hours=self._EXPIRATION_ADDED_TIME)

        return date.isoformat()
