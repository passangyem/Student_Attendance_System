import wx

# Create the application
app = wx.App()

# Create the main window
frame = wx.Frame(
    None,
    title="Hello World - wxPython",
    size=(400, 250)
)

# Create a panel
panel = wx.Panel(frame)

# Create a label
label = wx.StaticText(
    panel,
    label="Hello World!",
    pos=(140, 90)
)

# Set font size
font = wx.Font(
    18,
    wx.FONTFAMILY_DEFAULT,
    wx.FONTSTYLE_NORMAL,
    wx.FONTWEIGHT_NORMAL
)
label.SetFont(font)

# Display the window
frame.Show()

# Run the application
app.MainLoop()