#!/usr/bin/env python
# coding: utf-8

#pip install praw requsts
import praw
import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO)


def send_to_telegram(comment, toxiReport):
    telegram_url = os.environ['TELEGRAM_URL']
    telegram_post = {"chat_id": os.environ['TELEGRAM_CHAT_ID'], "text":  toxiReport[:-2] + "! Please check it out.\n\n" + "https://www.reddit.com" + comment.permalink + "\n\n-----\n" + comment.body}
    telegram_response = requests.post(telegram_url, json=telegram_post)
    logging.info("Telegram notification status code: " + str(telegram_response.status_code))


def send_to_slack(comment, toxiReport):
    slack_url = os.environ['SLACK_URL']
    slack_post = {"text":  toxiReport[:-2] + "! Please check it out.\n\n" + "https://www.reddit.com" + comment.permalink + "\n\n-----\n" + comment.body}
    slack_response = requests.post(slack_url, json=slack_post)
    logging.info("Slack notification status code: " + str(slack_response.status_code))


def console_log(response):
    response = response[0]
    logging.info("----------------")
    logging.info(response["text"].replace('\n', ''))
    logging.info("https://www.reddit.com" + comment.permalink)
    logging.info("identity_attack:\t" + json.dumps(response["identity_attack"]))
    logging.info("insult:\t\t" + json.dumps(response["insult"]))
    logging.info("obscene:\t\t" + json.dumps(response["obscene"]))
    logging.info("severe_toxicity:\t" + json.dumps(response["severe_toxicity"]))
    logging.info("sexual_explicit:\t" + json.dumps(response["sexual_explicit"]))
    logging.info("threat:\t\t" + json.dumps(response["threat"]))
    logging.info("toxicity:\t\t" + json.dumps(response["toxicity"]))


#def save_to_db():
    #TO DO


skip_existing_comments = False
report_to_telegram = False
report_to_slack = False

if os.environ['SKIP_EXISTING_COMMENTS'] == "True":
    skip_existing_comments = True

if os.environ['REPORT_TO_TELEGRAM'] == "True":
    report_to_telegram = True

if os.environ['REPORT_TO_SLACK'] == "True":
    report_to_slack = True

logging.info("REDDIT_CLIENT_ID: " + os.environ['REDDIT_CLIENT_ID'] + " type: " + type(os.environ['REDDIT_CLIENT_ID']).__name__)
logging.info("REDDIT_CLIENT_SECRET: " + os.environ['REDDIT_CLIENT_SECRET'] + " type: " + type(os.environ['REDDIT_CLIENT_SECRET']).__name__)
logging.info("SKIP_EXISTING_COMMENTS: " + os.environ['SKIP_EXISTING_COMMENTS'] + " type: " + type(os.environ['SKIP_EXISTING_COMMENTS']).__name__)
logging.info("skip_existing_comments: " + str(skip_existing_comments) + " type: " + type(skip_existing_comments).__name__)
logging.info("TOXI_API_URL: " + os.environ['TOXI_API_URL'] + " type: " + type(os.environ['TOXI_API_URL']).__name__)
logging.info("REPORT_TO_TELEGRAM: " + os.environ['REPORT_TO_TELEGRAM'] + " type: " + type(os.environ['REPORT_TO_TELEGRAM']).__name__)
logging.info("report_to_telegram: " + str(report_to_telegram) + " type: " + type(report_to_telegram).__name__)
logging.info("TELEGRAM_URL: " + os.environ['TELEGRAM_URL'] + " type: " + type(os.environ['TELEGRAM_URL']).__name__)
logging.info("TELEGRAM_CHAT_ID: " + os.environ['TELEGRAM_CHAT_ID'] + " type: " + type(os.environ['TELEGRAM_CHAT_ID']).__name__)
logging.info("REPORT_TO_SLACK: " + os.environ['REPORT_TO_SLACK'] + " type: " + type(os.environ['REPORT_TO_SLACK']).__name__)
logging.info("report_to_slack: " + str(report_to_slack) + " type: " + type(report_to_slack).__name__)
logging.info("SLACK_URL: " + os.environ['SLACK_URL'] + " type: " + type(os.environ['SLACK_URL']).__name__)

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent="iXsystems oAuth",
)


for comment in reddit.subreddit("truenas").stream.comments(skip_existing=skip_existing_comments):
    #print("https://www.reddit.com" + comment.permalink)
    #print(comment.body)
    api_url = os.environ['TOXI_API_URL']
    line = {"line": comment.body}
    response = requests.post(api_url, json=line)
    toxiReport = "Reddit comment possibly containing: "
    report = False;
    json_res = response.json()
    console_log(json_res)

    if json_res[0]["identity_attack"][0] != False:
        report = True
        toxiReport = toxiReport + "identity attack, "

    if json_res[0]["insult"][0] != False:
        report = True
        toxiReport = toxiReport + "insult, "

    if json_res[0]["obscene"][0] != False:
        report = True
        toxiReport = toxiReport + "obscenity, "

    if json_res[0]["severe_toxicity"][0] != False:
        report = True
        toxiReport = toxiReport + "severe toxicity, "

    if json_res[0]["sexual_explicit"][0] != False:
        report = True
        toxiReport = toxiReport + "explicit content, "

    if json_res[0]["threat"][0] != False:
        report = True
        toxiReport = toxiReport + "threat, "

    if json_res[0]["toxicity"][0] != False:
        report = True
        toxiReport = toxiReport + "general toxicity, "

    if report == True:
        if report_to_telegram == True:
            send_to_telegram(comment, toxiReport)

        if report_to_slack == True:
            send_to_slack(comment, toxiReport)





