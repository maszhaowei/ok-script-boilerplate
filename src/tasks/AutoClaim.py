from ok import TriggerTask
import re

liveEndText = "直播已结束"
claimText = "立即领取"
lotteryJoinTexts = ["立即参与", re.compile(r"^参与成功")]
lotteryResult = "查看中奖名单"

intervalKey = "检测间隔(秒)"
defaultInterval = 30


class AutoClaim(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动领取"
        self.default_config.update({intervalKey: defaultInterval})

    def run(self):
        self.log_info(self.hwnd_title)
        ocrBoxes = self.ocr(
            match=[liveEndText, claimText, lotteryResult] + lotteryJoinTexts
        )
        for ocrBox in ocrBoxes:
            self.log_info(ocrBox)
            if ocrBox.name == liveEndText:
                self.log_info(liveEndText, True)
            elif ocrBox.name == lotteryResult:
                closeBtn = self.find_one(
                    feature_name="closebutton", vertical_variance=5
                )
                if closeBtn:
                    self.log_info(f"Close button found by feature", True)
                    self.click_box(closeBtn)
            else:
                if ocrBox.name == claimText:
                    self.log_info(f"Claim button found by ocr", True)
                self.click_box(ocrBox)
        interval = self.config.get(intervalKey)
        self.sleep(max(interval, 1) if type(interval) is int else defaultInterval)
