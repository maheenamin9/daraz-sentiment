import json
import requests
from typing import List
from pycld2 import detect
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import parse
import os

start_date = datetime.fromisoformat('2020-07-01')
end_date = datetime.fromisoformat('2021-06-30')


class Category:
  def __init__(self, name: str, url: str = None):
    self.name = name
    self.url = url
    self.subcategories: List[Category] = []


def get_catergoies() -> List[Category]:
  daraz_homepage = requests.get('https://daraz.pk/').text
  soup = BeautifulSoup(daraz_homepage, 'html.parser')
  categories = soup.select('.lzd-site-menu-root-item')
  categories_list = []

  for category in categories:
    main_category = Category(category.select_one('a').text.strip())
    cat_css_id = category.attrs.get('id')
    anchor_tags = soup.select(f'.{cat_css_id} > li > a')

    for each in anchor_tags:
      cat_name = each.text
      cat_url = each.attrs['href']

      main_category.subcategories.append(
          Category(cat_name.strip(), 'https:' + cat_url + '?ajax=true'))

    categories_list.append(main_category)

  return categories_list


def get_review_url(item_id: int, page_no: int, page_size: int):
  return f'https://my.daraz.pk/pdp/review/getReviewList?itemId={item_id}&pageSize={page_size}&filter=0&sort=0&pageNo={page_no}'


categories = get_catergoies()

for index, each in enumerate(categories):
  print(f'{index + 1}. {each.name}')

index = int(input('> ')) - 1

total = 0

for subcatgory in categories[index].subcategories:
  print(f'Requesting {subcatgory.url}...')
  res = requests.get(subcatgory.url).json()
  total_prods = int(res['mainInfo']['totalResults'])
  pages = total_prods // 40 + 1
  try:
    for page_no in range(1, pages + 1):
      new_url = parse.urljoin(subcatgory.url, f'?ajax=true&page={page_no}')
      print(f'Requesting page {new_url}...')
      res = requests.get(new_url).json()
      products = res['mods']['listItems']
      for product in products:
        reviews_grabbed = 0

        item_id: int = product['nid']

        if (os.path.exists(f'data/{item_id}.json')):
          continue

        review_url = get_review_url(item_id, 1, 1000)
        review = requests.get(review_url).json()

        reviews_wanted = []

        if review['success']:
          review_items = review['model']['items']
          for review_item in review_items:
            review_content = review_item['reviewContent']
            review_time_str = review_item['reviewTime']
            try:
              review_time = datetime.strptime(review_time_str, '%d %b %Y')
              if review_time >= start_date and review_time <= end_date:
                if review_content:
                  is_reliable, _, details = detect(review_content)
                  if is_reliable and details[0][1] == 'en':
                    reviews_wanted.append(review_item)
                    reviews_grabbed += 1
            except ValueError:
              # i dont need the review as date will not be parseable to recent review
              # shown as 4 weeks ago, etc. I am fetching old reviews so i'll be fine
              pass

        if len(reviews_wanted) > 0:
          with open(f'data/{item_id}.json', 'w') as f:
            json.dump(reviews_wanted, f, indent=2)

        print(f'Grabbed {reviews_grabbed} reviews')
        total += reviews_grabbed
        print(f'Grabbed {total} in total')
  except KeyboardInterrupt:
    print('Moving to next category')
