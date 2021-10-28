import os, requests, json, logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# triggers modal popup when bot receives /sendpage command
@app.command("/sendpage")
def open_modal(ack, body, client):

    # Acknowledge the command request
    ack()

    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
	"title": {
		"type": "plain_text",
		"text": "Create Opsgenie Alert"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"type": "modal",
    "callback_id": "view_1",
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "divider"
		},
		{
			"type": "input",
			"block_id": "input_message",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alert Message"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Briefly summarize the problem"
				}
			]
		},
		{
			"type": "input",
			"block_id": "input_details",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Additional Details"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Add additional details like a link to the Slack or Zoom discussion. Please put 'none' for no other details."
				}
			]
		},
		{
			"type": "section",
			"block_id": "input_team",
			"text": {
				"type": "mrkdwn",
				"text": "*Team*"
			},
			"accessory": {
				"action_id": "multi_static_select-action",
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select Team(s) to receive the alert"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "ASER_Team"
						},
						"value": "ASER_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Android"
						},
						"value": "Android"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CameraBackend"
						},
						"value": "CameraBackend"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CameraCloud"
						},
						"value": "CameraCloud"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "App_QA"
						},
						"value": "App_QA"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Call_Center_Outage_Team"
						},
						"value": "Call_Center_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CSE"
						},
						"value": "CSE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "CURE"
						},
						"value": "CURE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Customer_Marketing_Outage_Team"
						},
						"value": "Customer_Marketing_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "DevOps_Team"
						},
						"value": "DevOps_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Drupal_Team"
						},
						"value": "Drupal_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "E-Commerce"
						},
						"value": "E-Commerce"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "FCP engineering"
						},
						"value": "FCP engineering"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "FIRE"
						},
						"value": "FIRE"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "International"
						},
						"value": "International"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "iOS"
						},
						"value": "iOS"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "IT"
						},
						"value": "IT"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Monitoring"
						},
						"value": "Monitoring"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Network"
						},
						"value": "Network"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "PR_Outage_Team"
						},
						"value": "PR_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Security"
						},
						"value": "Security"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Siren_Services"
						},
						"value": "Siren_Services"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Social_Media_Outage_Team"
						},
						"value": "Social_Media_Outage_Team"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "SS3 Core"
						},
						"value": "SS3 Core"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "UK_Team_Alerts"
						},
						"value": "UK_Team_Alerts"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "WebApp"
						},
						"value": "WebApp"
					}
				]
		    }
        }
	]
}
    )

# Handles the view_submission request
@app.view("view_1")
def handle_submission(ack, body, client, view, logger, error):
    alert_message = view["state"]["values"]["input_message"]["plain_text_input-action"]["value"]
    alert_team = view["state"]["values"]["input_team"]["multi_static_select-action"]["selected_options"]
    alert_details = view["state"]["values"]["input_details"]["plain_text_input-action"]["value"]
    user_id = body["user"]["id"]
    user = body["user"]["name"]
    opsgenie_api_key = os.environ.get('OPSGENIE_INTEGRATION_KEY')

    # Acknowledge the view_submission request and closes the modal
    ack()

    # Do whatever you want with the input data - here we're using the input data to send a create alert request to opsgenie
	# then sending the user a verification of their submission

    # Loop through the selected teams
    alert_responders = []
    for value in alert_team:
        alert_responders.append({
            'name': value['value'],
            'type': 'team'
        })

	#api requests to opsgenie
    headers = {
		'Authorization': f'GenieKey {opsgenie_api_key}',
		'Content-Type': 'application/json',
		}

    data = {
	'message': f'{alert_message} - {user}',
	'description': alert_details,
	'responders': alert_responders,
	'priority': 'P1'
	}

    data = json.dumps(data)

    response = requests.post('https://api.opsgenie.com/v2/alerts', headers=headers, data=data)

    # Add simple logging to track the success/failure of the requests
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info(f'Opsgenie API request returned an http status code {response.status_code}')

    # Message to send user
    try:
        if response.status_code == 202:
            msg = f"Hey {user}, your Opsgenie submission was successful!"
        else:
            msg = "There was a problem sending your request"
    except Exception as e:
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel=user_id, text=msg)
    except Exception as e:
        logger.exception(f"Failed to post a message {e}")


# Handles messages sent in a channel the bot is listening in that are not already handled above
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# Handles view event not already handled above
@app.view("view_1")
def handle_view_events(ack, body, logger):
    ack()
    logger.info(body)

# Handles multi select options event
@app.action("multi_static_select-action")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()