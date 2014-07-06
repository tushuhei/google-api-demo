#coding: utf8
import time
import csv
import re
import sys
from prettyprint import pp
from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


class Analytics:
  def __init__(self):
    self.service, self.flags = sample_tools.init(
        sys.argv, 'analytics', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/analytics.readonly')

  def print_profiles(self):
    accounts = self.service.management().accounts().list().execute()
    for account in accounts.get('items', []):
      webproperties = self.service.management().webproperties().list(accountId=account.get('id')).execute()
      for webproperty in webproperties.get('items', []):
        profiles = self.service.management().profiles().list(
            accountId=account.get('id'),
            webPropertyId=webproperty.get('id')).execute()
        for profile in profiles.get('items', []):
          print u'%s %s\t%s %s\t%s %s'%(account.get('id'), account.get('name'), webproperty.get('id'), webproperty.get('name'), profile.get('id'), profile.get('name'))
      time.sleep(1)


class AnalyticsProfile(Analytics):
  def __init__(self, profile_id):
    Analytics.__init__(self)
    self.profile_id = profile_id

  def get_homepage_pageviews(self, start_date, end_date):
    return self.service.data().ga().get(
        ids='ga:%d'%self.profile_id,
        start_date=start_date,
        end_date=end_date,
        metrics='ga:pageviews',
        dimensions='ga:pagePath',
        filters='ga:pagePath=~^/index.php\?id\=\d+',
        sort='-ga:pageviews',
        samplingLevel='HIGHER_PRECISION').execute()

  def get_date_pageviews(self, start_date, end_date):
    return self.service.data().ga().get(
        ids='ga:%d'%self.profile_id,
        start_date=start_date,
        end_date=end_date,
        metrics='ga:pageviews',
        dimensions='ga:date',
        sort='-ga:pageviews',
        samplingLevel='HIGHER_PRECISION').execute()

  def get_homepage_adsenserevenue(self, start_date, end_date):
    return self.service.data().ga().get(
        ids='ga:%d'%self.profile_id,
        start_date=start_date,
        end_date=end_date,
        metrics='ga:adsenseRevenue',
        dimensions='ga:pagePath',
        filters='ga:pagePath=~^/index.php\?id\=\d+',
        samplingLevel='HIGHER_PRECISION').execute()


class Adsense:
  def __init__(self):
    self.service, self.flags = sample_tools.init(
        sys.argv, 'adsense', 'v1.4', __doc__, __file__, parents=[],
        scope='https://www.googleapis.com/auth/adsense.readonly')

  def print_accounts(self):
    accounts = self.service.accounts().list().execute()
    for account in accounts.get('items'):
      print account


class AdsenseAccount(Adsense):
  def __init__(self, ad_client_id):
    Adsense.__init__(self)
    self.ad_client_id = ad_client_id

  def get_daily_performance(self, start_date, end_date):
    return self.service.reports().generate(
        startDate=start_date,
        endDate=end_date,
        filter=['AD_CLIENT_ID==%s'%(self.ad_client_id)],
        metric=['PAGE_VIEWS','CLICKS','COST_PER_CLICK','PAGE_VIEWS_CTR','PAGE_VIEWS_RPM','EARNINGS'],
        dimension=['DATE'],
        sort=['-DATE']).execute()


def main():
  ga = Analytics()
  ga.print_profiles()

if __name__ == '__main__':
  main()



