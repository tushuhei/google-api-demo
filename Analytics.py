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

  def get_pageviews(self, start_date, end_date, start=1, count=5000):
    return self.service.data().ga().get(
        ids='ga:%d'%self.profile_id,
        start_date=start_date,
        end_date=end_date,
        metrics='ga:pageviews',
        dimensions='ga:pagePath',
        filters='ga:pagePath=~^/index.php\?id\=\d+',
        sort='-ga:pageviews',
        max_results=str(count),
        start_index=str(start),
        samplingLevel='HIGHER_PRECISION').execute()

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

def main():
  ga = Analytics()
  ga.print_profiles()

if __name__ == '__main__':
  main()



