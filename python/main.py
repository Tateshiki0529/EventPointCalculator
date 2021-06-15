import wx, math, webbrowser

versusContPointList = [60, 52, 44, 37, 30]
APPVERSION = "1.1.0"

def selectEventType(e):
	obj = e.GetEventObject()
	eventType = obj.GetClientData(obj.GetSelection())
	eventPanelVisibleToggle(eventType)
	if eventType == "challenge":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("フリーライブ", "free")
		calcPanelLiveTypeListbox.Append("チャレンジライブ(Beta)", "challenge")
		calcPanelLiveTypeListbox.Enable()
	elif eventType == "versus":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	elif eventType == "livetry":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	elif eventType == "mission":
		calcPanelLiveTypeListbox.Clear()
		calcPanelLiveTypeListbox.Append("⚠ 対応していません! ⚠", None)
		calcPanelLiveTypeListbox.Disable()
	calcPanel.Layout()

def selectLiveType(e):
	obj = e.GetEventObject()
	eventType = obj.GetClientData(obj.GetSelection())
	calculate(None)

def calculate(e):
	eventType = calcPanelEventTypeListbox.GetClientData(calcPanelEventTypeListbox.GetSelection())

	if eventType == "challenge":
		try:
			liveType = calcPanelLiveTypeListbox.GetClientData(calcPanelLiveTypeListbox.GetSelection())
			eventPoint = calcPanelChallengeEventPointInput.GetValue()
			if liveType == "free":
				scoreMin = (eventPoint - 20) * 25000
				scoreMax = scoreMin + 24999
			elif liveType == "challenge":
				scoreMin = eventPoint - 1000
				scoreMin *= 300
				scoreMax = scoreMin + 24999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "versus":
		try:
			eventPoint = calcPanelVersusEventPointInput.GetValue()
			contributePoint = calcPanelVersusContributePointOutput.GetValue()
			scoreMin = (eventPoint - contributePoint) * 5500
			scoreMax = scoreMin + 5499
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "livetry":
		try:
			eventPoint = calcPanelLiveTryEventPointInput.GetValue()
			scoreMin = (eventPoint - 40) * 13000
			scoreMax = scoreMin + 12999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			resultPanelCalcOutput.SetValue("入力が不足しています")
	elif eventType == "mission":
		try:
			eventPoint = calcPanelMissionEventPointInput.GetValue()
			SBPower = calcPanelMissionSBPowerInput.GetValue()
			scoreMin = (eventPoint - 40 - math.floor(SBPower / 3000)) * 10000
			scoreMax = scoreMin + 9999
			resultPanelCalcOutput.SetValue("{:,}".format(scoreMin)+" ～ "+"{:,}".format(scoreMax))
		except wx._core.wxAssertionError:
			resultPanelCalcOutput.SetValue("入力が不足しています")
	if scoreMax < 0:
		resultPanelCalcOutput.AppendText(" (調整不可)")
def eventPanelVisibleToggle(eventType):
	calcPanelChallengeEventPanel.Hide()
	calcPanelVersusEventPanel.Hide()
	calcPanelLiveTryEventPanel.Hide()
	calcPanelMissionEventPanel.Hide()
	if eventType == "challenge":
		calcPanelChallengeEventPanel.Show()
	elif eventType == "versus":
		calcPanelVersusEventPanel.Show()
	elif eventType == "livetry":
		calcPanelLiveTryEventPanel.Show()
	elif eventType == "mission":
		calcPanelMissionEventPanel.Show()
	calcPanel.Layout()

def changeCPParticipantsCount(e):
	participantsCount = calcPanelVersusContributePointParticipantsCount.GetClientData(calcPanelVersusContributePointParticipantsCount.GetSelection())
	if participantsCount == 2:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 3)
		calcPanelVersusContributePointRankListbox.Append("2位", 4)
	elif participantsCount == 3:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 2)
		calcPanelVersusContributePointRankListbox.Append("2位", 3)
		calcPanelVersusContributePointRankListbox.Append("3位", 4)
	elif participantsCount == 4:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 1)
		calcPanelVersusContributePointRankListbox.Append("2位", 2)
		calcPanelVersusContributePointRankListbox.Append("3位", 3)
		calcPanelVersusContributePointRankListbox.Append("4位", 4)
	elif participantsCount == 5:
		calcPanelVersusContributePointRankListbox.Clear()
		calcPanelVersusContributePointRankListbox.Append("1位", 0)
		calcPanelVersusContributePointRankListbox.Append("2位", 1)
		calcPanelVersusContributePointRankListbox.Append("3位", 2)
		calcPanelVersusContributePointRankListbox.Append("4位", 3)
		calcPanelVersusContributePointRankListbox.Append("5位", 4)
	calcPanelVersusContributePointRankListbox.SetSelection(0)
	calcPanelVersusContributePointOutput.SetValue(versusContPointList[0])
	calcPanelVersusContributePointEventPanel.Layout()
	calcPanelVersusEventPanel.Layout()
	calculate(None)

def calculateCP(e):
	participantsCount = calcPanelVersusContributePointParticipantsCount.GetClientData(calcPanelVersusContributePointParticipantsCount.GetSelection())
	try:
		pointIndex = calcPanelVersusContributePointRankListbox.GetClientData(calcPanelVersusContributePointRankListbox.GetSelection())
	except wx._core.wxAssertionError:
		pointIndex = 0
	calcPanelVersusContributePointOutput.SetValue(versusContPointList[pointIndex])
	calcPanelVersusContributePointEventPanel.Layout()
	calcPanelVersusEventPanel.Layout()
	calculate(None)

def urlClick1(e):
	if e.LeftUp():
		webbrowser.open("https://twitter.com/@T_BanGDreamer")
	e.Skip()

def urlClick2(e):
	if e.LeftUp():
		webbrowser.open("https://gbp.epcalc.ml/")
	e.Skip()

def resourcePath(path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, path)
	return os.path.join(os.path.abspath("."), path)

if __name__ == "__main__":
	app = wx.App()
	frame = wx.Frame(None, wx.ID_ANY, "EventPointCalculator for Python", size=(500, 450))
	frame.CreateStatusBar()
	frame.SetStatusText('EventPointCalculator Ready.')

	notebook = wx.Notebook(frame, wx.ID_ANY)

	# ページ1. 計算
	
	# ページパネル (親: notebook)
	pagePanel1 = wx.Panel(notebook, wx.ID_ANY)

	# 計算パラメータ等入力パネル (親: pagePanel1)
	calcPanel = wx.Panel(pagePanel1, wx.ID_ANY)
	calcPanel.SetBackgroundColour("#fff")
	
	# イベントタイプ選択用パネル (親: calcPanel)
	calcPanelEventTypePanel = wx.Panel(calcPanel, wx.ID_ANY)

	# イベントタイプ選択用リストボックス (親: calcPanelEventTypePanel)
	calcPanelEventTypeListbox = wx.ListBox(calcPanelEventTypePanel, wx.ID_ANY, style=wx.LB_SINGLE)
	calcPanelEventTypeListbox.Append("チャレンジライブイベント", "challenge")
	calcPanelEventTypeListbox.Append("対バンライブイベント", "versus")
	calcPanelEventTypeListbox.Append("ライブトライ！イベント", "livetry")
	calcPanelEventTypeListbox.Append("ミッションライブイベント", "mission")
	calcPanelEventTypeListbox.Bind(wx.EVT_LISTBOX, selectEventType)
	
	# ライブ種別選択用リストボックス (親: calcPanelEventTypePanel)
	calcPanelLiveTypeListbox = wx.ListBox(calcPanelEventTypePanel, wx.ID_ANY, style=wx.LB_SINGLE)
	calcPanelLiveTypeListbox.Append("⚠ イベントタイプを指定してください! ⚠", None)
	calcPanelLiveTypeListbox.Bind(wx.EVT_LISTBOX, selectLiveType)

	# イベントタイプ選択用パネル構成レイアウト (親: calcPanelEventTypePanel)
	calcPanelEventTypeLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelEventTypeLayout.Add(wx.StaticText(calcPanelEventTypePanel, wx.ID_ANY, "イベント種別"))
	calcPanelEventTypeLayout.Add(calcPanelEventTypeListbox, flag=wx.EXPAND | wx.ALL, border=3)
	calcPanelEventTypeLayout.Add(wx.StaticText(calcPanelEventTypePanel, wx.ID_ANY, "ライブ種別"))
	calcPanelEventTypeLayout.Add(calcPanelLiveTypeListbox, flag=wx.EXPAND | wx.ALL, border=3)
	calcPanelEventTypePanel.SetSizer(calcPanelEventTypeLayout)

	# ------------------------------

	# チャレンジライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelChallengeEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# チャレンジライブイベント用目標ポイント入力ボックス (親: calcPanelChallengeEventPanel)
	calcPanelChallengeEventPointInput = wx.SpinCtrl(calcPanelChallengeEventPanel, wx.ID_ANY)
	calcPanelChallengeEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelChallengeEventPointInput.SetMax(100000)
	calcPanelChallengeEventPointInput.SetMin(0)

	# チャレンジライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelChallengeEventPanel)
	calcPanelChallengeEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelChallengeEventLayout.Add(wx.StaticText(calcPanelChallengeEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelChallengeEventLayout.Add(calcPanelChallengeEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelChallengeEventPanel.SetSizer(calcPanelChallengeEventLayout)

	# -------------------------------------

	# 対バンライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelVersusEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# 対バンライブイベント用目標ポイント入力ボックス (親: calcPanelVersusEventPanel)
	calcPanelVersusEventPointInput = wx.SpinCtrl(calcPanelVersusEventPanel, wx.ID_ANY)
	calcPanelVersusEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelVersusEventPointInput.SetMax(100000)
	calcPanelVersusEventPointInput.SetMin(0)

	# ----------------

	# 対バンライブ貢献度ポイント計算パネル (親: calcPanelVersusEventPanel)
	calcPanelVersusContributePointEventPanel = wx.Panel(calcPanelVersusEventPanel, wx.ID_ANY)

	# 対バンライブ貢献ポイント計算用参加人数入力ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointParticipantsCount = wx.ListBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointParticipantsCount.Bind(wx.EVT_LISTBOX, changeCPParticipantsCount)
	calcPanelVersusContributePointParticipantsCount.Append("2人", 2)
	calcPanelVersusContributePointParticipantsCount.Append("3人", 3)
	calcPanelVersusContributePointParticipantsCount.Append("4人", 4)
	calcPanelVersusContributePointParticipantsCount.Append("5人", 5)
	calcPanelVersusContributePointParticipantsCount.SetSelection(3)

	# 対バンライブ貢献ポイント計算用貢献順位入力ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointRankListbox = wx.ListBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointRankListbox.Bind(wx.EVT_LISTBOX, calculateCP)
	calcPanelVersusContributePointRankListbox.Append("1位", 0)
	calcPanelVersusContributePointRankListbox.Append("2位", 1)
	calcPanelVersusContributePointRankListbox.Append("3位", 2)
	calcPanelVersusContributePointRankListbox.Append("4位", 3)
	calcPanelVersusContributePointRankListbox.Append("5位", 4)
	calcPanelVersusContributePointRankListbox.SetSelection(0)

	# 対バンライブ貢献ポイント表示ボックス (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointOutput = wx.SpinCtrl(calcPanelVersusContributePointEventPanel, wx.ID_ANY)
	calcPanelVersusContributePointOutput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelVersusContributePointOutput.SetMin(30)
	calcPanelVersusContributePointOutput.SetMax(60)
	calcPanelVersusContributePointOutput.SetValue(60)
	calcPanelVersusContributePointOutput.Disable()

	# 対バンライブ貢献度ポイント計算パネル構成レイアウト (親: calcPanelVersusContributePointEventPanel)
	calcPanelVersusContributePointEventBox = wx.StaticBox(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ポイント関係")

	calcPanelVersusContributePointEventLayout = wx.StaticBoxSizer(calcPanelVersusContributePointEventBox, wx.VERTICAL)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "参加人数"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointParticipantsCount, flag=wx.EXPAND | wx.ALL, border=2)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ランキング"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointRankListbox, flag=wx.EXPAND | wx.ALL, border=2)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "参加人数"))
	calcPanelVersusContributePointEventLayout.Add(wx.StaticLine(calcPanelVersusContributePointEventPanel), flag=wx.GROW)
	calcPanelVersusContributePointEventLayout.Add(wx.StaticText(calcPanelVersusContributePointEventPanel, wx.ID_ANY, "貢献度ポイント"))
	calcPanelVersusContributePointEventLayout.Add(calcPanelVersusContributePointOutput, flag=wx.EXPAND | wx.ALL, border=2)

	calcPanelVersusContributePointEventPanel.SetSizer(calcPanelVersusContributePointEventLayout)

	# ----------------

	# 対バンライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelVersusEventPanel)
	calcPanelVersusEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelVersusEventLayout.Add(wx.StaticText(calcPanelVersusEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelVersusEventLayout.Add(calcPanelVersusEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)
	calcPanelVersusEventLayout.Add(calcPanelVersusContributePointEventPanel,  flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelVersusEventPanel.SetSizer(calcPanelVersusEventLayout)

	# -------------------------------

	# ミッションライブイベント用パラメータ入力パネル (親: calcPanel)
	calcPanelMissionEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# ミッションライブイベント用目標ポイント入力ボックス (親: calcPanelMissionEventPanel)
	calcPanelMissionEventPointInput = wx.SpinCtrl(calcPanelMissionEventPanel, wx.ID_ANY)
	calcPanelMissionEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelMissionEventPointInput.SetMax(100000)
	calcPanelMissionEventPointInput.SetMin(0)

	# ----------------

	# ミッションライブイベントSB総合力入力パネル (親: calcPanelMissionEventPanel)
	calcPanelMissionSBPowerInputPanel = wx.Panel(calcPanelMissionEventPanel, wx.ID_ANY)

	# ミッションライブイベントSB総合力入力ボックス (親: calcPanelMissionSBPowerInputPanel)
	calcPanelMissionSBPowerInput = wx.SpinCtrl(calcPanelMissionSBPowerInputPanel, wx.ID_ANY)
	calcPanelMissionSBPowerInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelMissionSBPowerInput.SetMin(0)
	calcPanelMissionSBPowerInput.SetMax(1000000)
	calcPanelMissionSBPowerInput.SetValue(150000)

	# ミッションライブイベントSB総合力入力パネル構成レイアウト (親: calcPanelMissionSBPowerInputPanel)
	calcPanelMissionSBPowerInputBox = wx.StaticBox(calcPanelMissionSBPowerInputPanel, wx.ID_ANY, "SB総合力")

	calcPanelMissionSBPowerInputLayout = wx.StaticBoxSizer(calcPanelMissionSBPowerInputBox, wx.VERTICAL)
	calcPanelMissionSBPowerInputLayout.Add(wx.StaticText(calcPanelMissionSBPowerInputPanel, wx.ID_ANY, "サポートバンドの総合力"))
	calcPanelMissionSBPowerInputLayout.Add(calcPanelMissionSBPowerInput, flag=wx.EXPAND | wx.ALL, border=2)

	calcPanelMissionSBPowerInputPanel.SetSizer(calcPanelMissionSBPowerInputLayout)

	# ----------------

	# ミッションライブイベント用パラメータ入力パネル構成レイアウト (親: calcPanelMissionEventPanel)
	calcPanelMissionEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelMissionEventLayout.Add(wx.StaticText(calcPanelMissionEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelMissionEventLayout.Add(calcPanelMissionEventPointInput, flag=wx.EXPAND | wx.ALL, border=5)
	calcPanelMissionEventLayout.Add(calcPanelMissionSBPowerInputPanel,  flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelMissionEventPanel.SetSizer(calcPanelMissionEventLayout)

	# -------------------------------

	# ライブトライ！イベント用パラメータ入力パネル (親: calcPanel)
	calcPanelLiveTryEventPanel = wx.Panel(calcPanel, wx.ID_ANY)

	# ライブトライ！イベント用目標ポイント入力ボックス (親: calcPanelLiveTryEventPanel)
	calcPanelLiveTryEventPointInput = wx.SpinCtrl(calcPanelLiveTryEventPanel, wx.ID_ANY)
	calcPanelLiveTryEventPointInput.Bind(wx.EVT_SPINCTRL, calculate)
	calcPanelLiveTryEventPointInput.SetMax(100000)
	calcPanelLiveTryEventPointInput.SetMin(0)

	# ライブトライ！イベント用パラメータ入力パネル構成レイアウト (親: calcPanelLiveTryEventPanel)
	calcPanelLiveTryEventLayout = wx.BoxSizer(wx.VERTICAL)
	calcPanelLiveTryEventLayout.Add(wx.StaticText(calcPanelLiveTryEventPanel, wx.ID_ANY, "欲しいイベントポイント数"))
	calcPanelLiveTryEventLayout.Add(calcPanelLiveTryEventPointInput, flag=wx.EXPAND | wx.ALL, border=3)

	calcPanelLiveTryEventPanel.SetSizer(calcPanelLiveTryEventLayout)

	# -------------------------------

	# 計算パラメータ等入力パネル構成レイアウト (親: calcPanel)
	calcPanelBox = wx.StaticBox(calcPanel, wx.ID_ANY, "パラメータ")

	calcPanelLayout = wx.StaticBoxSizer(calcPanelBox, wx.HORIZONTAL)
	calcPanelLayout.Add(calcPanelEventTypePanel)
	calcPanelLayout.Add(calcPanelChallengeEventPanel)
	calcPanelLayout.Add(calcPanelVersusEventPanel)
	calcPanelLayout.Add(calcPanelLiveTryEventPanel)
	calcPanelLayout.Add(calcPanelMissionEventPanel)

	calcPanel.SetSizer(calcPanelLayout)

	# ライブ種別リストボックス無効化
	calcPanelLiveTypeListbox.Disable()

	# 全入力パネルを隠す
	calcPanelChallengeEventPanel.Hide()
	calcPanelVersusEventPanel.Hide()
	calcPanelLiveTryEventPanel.Hide()
	calcPanelMissionEventPanel.Hide()
	calcPanel.Layout()

	# 計算結果表示パネル (親: pagePanel1)
	resultPanel = wx.Panel(pagePanel1, wx.ID_ANY)
	resultPanel.SetBackgroundColour("#fff")

	# 計算結果テキスト表示ボックス (親: resultPanel)
	resultPanelCalcOutput = wx.TextCtrl(resultPanel, wx.ID_ANY, "入力待ち…", style=wx.TE_CENTER, size=(250, -1))

	# 計算結果表示パネル構成レイアウト (親: resultPanel)
	resultPanelBox = wx.StaticBox(resultPanel, wx.ID_ANY, "計算結果")
	resultPanelLayout = wx.StaticBoxSizer(resultPanelBox, wx.HORIZONTAL)
	resultPanelLayout.Add(wx.StaticText(resultPanel, wx.ID_ANY, "獲得すべきライブスコア: "), flag=wx.GROW | wx.EXPAND | wx.TOP | wx.LEFT, border=6)
	resultPanelLayout.Add(resultPanelCalcOutput, flag=wx.GROW | wx.EXPAND | wx.TOP | wx.BOTTOM, border=3)

	resultPanel.SetSizer(resultPanelLayout)

	# ページパネル構成レイアウト (親: pagePanel1)
	pagePanel1Layout = wx.FlexGridSizer(rows=2, cols=1, gap=(0, 0))
	pagePanel1Layout.Add(calcPanel, proportion=1, flag=wx.GROW | wx.EXPAND | wx.ALL, border=7)
	pagePanel1Layout.Add(resultPanel, proportion=1, flag=wx.GROW | wx.EXPAND | wx.ALL, border=7)
	pagePanel1Layout.AddGrowableRow(0)
	pagePanel1Layout.AddGrowableCol(0)

	pagePanel1.SetSizer(pagePanel1Layout)
	# ページ1ここまで

	# ページ2. About (親: notebook)
	pagePanel2 = wx.Panel(notebook, wx.ID_ANY)

	pagePanel2Layout = wx.BoxSizer(wx.VERTICAL)
	aboutPanelUrlTextTwitter = wx.StaticText(pagePanel2, wx.ID_ANY, "by @T_BanGDreamer")
	aboutPanelUrlTextTwitter.Bind(wx.EVT_MOUSE_EVENTS, urlClick1)
	aboutPanelUrlTextTwitter.Bind(wx.EVT_MOTION, urlClick1)
	font = wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.FONTWEIGHT_LIGHT, True)
	aboutPanelUrlTextTwitter.SetFont(font)
	aboutPanelUrlTextTwitter.SetForegroundColour('#0000ff')
	aboutPanelUrlTextWeb = wx.StaticText(pagePanel2, wx.ID_ANY, "https://gbp.epcalc.ml/")
	aboutPanelUrlTextWeb.Bind(wx.EVT_MOUSE_EVENTS, urlClick2)
	aboutPanelUrlTextWeb.Bind(wx.EVT_MOTION, urlClick2)
	font2 = wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.FONTWEIGHT_LIGHT, True)
	aboutPanelUrlTextWeb.SetFont(font2)
	aboutPanelUrlTextWeb.SetForegroundColour('#0000ff')
	for i in range(0, 9):
		pagePanel2Layout.Add(wx.StaticText(pagePanel2, wx.ID_ANY, ""))
	pagePanel2Layout.Add(wx.StaticText(pagePanel2, wx.ID_ANY, "EventPointCalculator for Python v"+APPVERSION), flag=wx.ALIGN_CENTER, border=3)
	pagePanel2Layout.Add(aboutPanelUrlTextTwitter, flag=wx.ALIGN_CENTER, border=3)
	pagePanel2Layout.Add(wx.StaticText(pagePanel2, wx.ID_ANY, ""))
	pagePanel2Layout.Add(aboutPanelUrlTextWeb, flag=wx.ALIGN_CENTER, border=3)
	pagePanel2.SetSizer(pagePanel2Layout)

	# ページ2ここまで

	notebook.InsertPage(0, pagePanel1, "計算")
	notebook.InsertPage(1, pagePanel2, "About")

	icon = wx.Icon(resourcePath('logo.ico'), wx.BITMAP_TYPE_ICO)
	frame.SetIcon(icon)

	frame.Show()
	app.MainLoop()