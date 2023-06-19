class Config():
    def config(self):
        # Starting page from which the scraping starts: e.g "all snakes for sale"
        page1 = ''
        # page2 = ''
        # page3 = ''

        pages = [page1]


        # CSS or XPath selector for catogories within starting page. 
        # Used if the items on sale are allocated to different categories within the starting page, e.g. "Boas"  
        # Not in text mode 
        category_card = None

        category_card_2 = None

        # CSS or XPath selector that indicates the html code for an item on sale
        item_card = ''

        # CSS or XPath selector for deeper lever page links (href), e.g. link to category and link to item page
        # e.g. h4.card-title a::attr(href)
        inner_page_href_1 = ''
        inner_page_href_2 = ''
        inner_page_href_3 = ''

        # List deeper level page links here.
        # List only if page is used.
        inner_page_href = [inner_page_href_1]
        

        # Text element from CSS or XPath selectors for each html section within item card or inner item page that indicates the field in question
        # e.g. div.alt1::text
        # type in fields are given as a list e.g. location = ['USA']
        timestamp = ''
        location = ''
        other = ''
        quantity = ''
        reptile = ''
        price = ''
        image = ''
        description = ''
        comments = ''
        seller = ''
        commenter = ''
        intent = ''
        website_type = ''
                

        # CSS or XPath selector for next page links (href) e.g. li.pagination-item--next a::attr(href)'
        # Used if items are listed in more than one page and a "next page" link is found on the page
        next_page_href = None

        # If paging is needed fill the following
        starting_page = None    # The number used in the page url to indicate the page after the first page
        last_page = None        # The number used in the page url to indicate the last page
        paging_interval = None  # Interval between pages, usually 1
        paging_string_1 = ''    # In the page url the string that is added to the base url before the page number
        paging_string_2 = ''    # In the page url the string that is added to the base url after the page number

        # Fields that are found on the same page leve with "item_card"
        first_page_fields = {
            'timestamp' : None,
            'reptile' : None,
            'price' : None,
            'quantity' : None,
            'description' : None,
            'comments' : None,
            'location' : None,
            'other' : None,
            'image' : None,
            'seller' : None,
            'commenter' : None,
            'intent' : None,
            'website_type': None                         
        }

        # Fields that are found on inner page describing the item on sale
        inner_page_fields = {
            'timestamp' : None,
            'reptile' : None,
            'price' : None,
            'quantity' : None,
            'description' : None,
            'comments' : None,
            'location' : None,
            'other' : None,
            'image' : None,
            'seller' : None,
            'commenter' : None,
            'intent' : None,
            'website_type': None                  
        }

        # Fields that are not scraped but known by the user e.g. location of the shop
        type_in_fields = {
            'timestamp' : None,
            'reptile' : None,
            'price' : None,
            'quantity' : None,
            'description' : None,
            'comments' : None,
            'location' : None,
            'other' : None,
            'image' : None,
            'seller' : None,
            'commenter' : None,
            'intent' : None,
            'website_type': None                        
        }

        return pages, category_card, category_card_2, inner_page_href, item_card, first_page_fields, inner_page_fields, type_in_fields, next_page_href, starting_page, last_page, paging_interval, paging_string_1, paging_string_2

    def download_delay(self):
        download_delay = 0
        return download_delay