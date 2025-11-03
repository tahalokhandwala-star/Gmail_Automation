# 🚀 RFQ Automation System with Real-Time Dashboard

Automated Request for Quotation (RFQ) processing system that monitors Gmail, extracts information using AI, manages customer database, updates tracking spreadsheets, and sends automatic acknowledgments.

## ✨ Features

- 📧 **Real-time Gmail Monitoring** - Detects new RFQ emails instantly via Google Pub/Sub
- 🤖 **AI-Powered Parsing** - Extracts client details using OpenAI GPT
- 🗄️ **Customer Database** - Tracks new and existing clients automatically
- 📊 **Google Sheets Integration** - Logs all RFQs to centralized tracking sheet
- ✉️ **Auto-Acknowledgment** - Sends professional replies automatically
- 🎨 **Beautiful Dashboard** - Real-time flowchart visualization with Streamlit

## 🎬 Live Dashboard

The flowchart dashboard shows all 4 automation steps in real-time:

```
Step 1: Processing New RFQ Email
   ↓
Step 2: Checking Customer Database
   ↓
Step 3: Updating Google Spreadsheet
   ↓
Step 4: Sending Acknowledgment
```

Each step shows:
- ⏳ Pending (grey) → ⚙️ Processing (blue animation) → ✅ Completed (green)
- Live business logs
- Smooth animations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_key
SPREADSHEET_ID=your_google_sheet_id
PUBSUB_PROJECT_ID=your_gcp_project
PUBSUB_SUBSCRIPTION_NAME=gmail-sub
```

### 3. Set Up Google Credentials
- Place `credentials.json` from Google Cloud Console in project root
- Run once to generate `token.json`

### 4. Run Dashboard
```bash
streamlit run flowchart_demo.py
```

Or use the launcher:
```bash
python run_flowchart.py
```

## 📁 Project Structure

```
Gmail_Automation/
├── flowchart_demo.py      # Main dashboard
├── main.py                # Automation engine
├── gmail_service.py       # Gmail API integration
├── llm_parser.py          # OpenAI parsing
├── db_manager.py          # SQLite database
├── sheets_service.py      # Google Sheets API
├── config.py              # Configuration
├── run_flowchart.py       # Simple launcher
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## 🔧 Configuration

### Gmail Setup
1. Enable Gmail API in Google Cloud Console
2. Set up Pub/Sub notifications
3. Download OAuth credentials
4. Run authentication flow

### OpenAI Setup
1. Get API key from platform.openai.com
2. Add to `.env` file

### Google Sheets Setup
1. Create a Google Sheet
2. Share with service account email
3. Copy Sheet ID to `.env`

## 💻 Usage

### Run Automation (Background)
```bash
python main.py
```

### Run with Dashboard (Recommended)
```bash
streamlit run flowchart_demo.py
```
Then click "🚀 Start Automation" in the browser.

### Dashboard Features
- **Start/Stop Automation** - Control automation with buttons
- **Real-Time Updates** - See each step as it processes
- **Live Logs** - View business-specific events
- **Visual Indicators** - Color-coded step status
- **Process Info** - Monitor PIDs and system status

## 📊 Workflow

1. **Email Detection**
   - Monitors Gmail for RFQ emails
   - Filters by subject keywords (quotation, quote, RFQ)
   - Detects new emails in real-time

2. **AI Parsing**
   - Extracts client name, email, phone, project details
   - Uses GPT-4 for intelligent parsing
   - Handles various email formats

3. **Database Check**
   - Searches for existing customer
   - Adds new clients automatically
   - Retrieves customer history

4. **Spreadsheet Update**
   - Logs RFQ to Google Sheets
   - Includes ENQ number, date, client info
   - Updates status and priority

5. **Acknowledgment**
   - Sends professional auto-reply
   - Thanks customer for inquiry
   - Confirms receipt and next steps

## 🎨 Dashboard Preview

The dashboard shows:
- **Control Panel**: Start/Stop buttons + Status indicator
- **Metrics Row**: RFQs processed, steps completed, active/pending
- **Workflow Steps**: 4 animated boxes showing current state
- **Live Output**: Real-time process logs
- **Debug Info**: Process IDs and system diagnostics

## 🔍 Troubleshooting

### Dashboard Not Starting
```bash
# Check Streamlit installation
pip install streamlit streamlit-autorefresh

# Run directly
streamlit run flowchart_demo.py
```

### Automation Not Processing
- Verify Gmail credentials (credentials.json, token.json)
- Check .env configuration
- Ensure Pub/Sub subscription exists
- Look for errors in console output

### Steps Not Updating
- Check temp_automation_log.txt is being created
- Verify main.py is running
- Look at terminal output for EVENT markers

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `SPREADSHEET_ID` | Google Sheet ID | `1a2b3c...` |
| `PUBSUB_PROJECT_ID` | GCP Project ID | `my-project-123` |
| `PUBSUB_SUBSCRIPTION_NAME` | Pub/Sub subscription | `gmail-sub` |

## 🛠️ Development

### Adding New Features
1. Modify `main.py` for automation logic
2. Add EVENT markers for dashboard integration
3. Update `flowchart_demo.py` to handle new events
4. Test with real emails

### Event System
The dashboard reads these EVENT markers from main.py:
```python
print("EVENT:FETCHING_EMAILS:START")     # Step 1 starts
print("EVENT:FETCHING_EMAILS:COMPLETE")  # Step 1 done
print("EVENT:LLM_PARSE:COMPLETE")        # Step 2 starts
print("EVENT:SHEET_UPDATE:COMPLETE")     # Step 3 starts
print("EVENT:ACK_EMAIL:COMPLETE")        # Step 4 starts
```

## 📦 Dependencies

- `streamlit` - Dashboard framework
- `streamlit-autorefresh` - Auto-refresh for live updates
- `google-auth` - Google authentication
- `google-api-python-client` - Gmail & Sheets APIs
- `google-cloud-pubsub` - Real-time notifications
- `openai` - AI parsing
- `python-dotenv` - Environment management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 🎯 Roadmap

- [ ] Add email templates customization
- [ ] Support multiple email accounts
- [ ] Advanced filtering rules
- [ ] Analytics dashboard
- [ ] Mobile notifications
- [ ] API endpoints

## 💡 Tips

### For Demo/Presentations
1. Delete `processed_email_ids.txt` to reprocess test emails
2. Send a test RFQ with keywords in subject
3. Click "Start Automation" in dashboard
4. Watch the beautiful step-by-step animation!

### For Production
1. Set up proper error handling
2. Configure email templates
3. Adjust polling frequency (default: 30 seconds)
4. Monitor logs regularly
5. Back up database periodically

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in console output
3. Verify all credentials are set up
4. Check `.env` configuration

## 🙏 Acknowledgments

Built with:
- Streamlit for beautiful dashboards
- OpenAI for intelligent parsing
- Google Cloud for Gmail & Sheets APIs

---

**Made with ❤️ for automating RFQ workflows**

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready ✅
