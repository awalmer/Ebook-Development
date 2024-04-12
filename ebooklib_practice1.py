# python3 -m pip install ebooklib
import ebooklib
from ebooklib import epub
# read html
from bs4 import BeautifulSoup 


# Read EPUB
# See if the EPUB file I exported from InDesign reads:
book_read = epub.read_epub('InDesign Practice Book.epub', {"ignore_ncx": True})
items = list(book_read.get_items_of_type(ebooklib.ITEM_DOCUMENT))
'''
for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
    print(image)
'''

# Writing EPUB
book = epub.EpubBook()
print(book)

# set metadata
book.add_metadata('DC', 'description', 'This is description for my book')
book.add_metadata(None, 'meta', '', {'name': 'key', 'content': 'value'})

book.set_identifier("id1234")
book.set_title("Ni, A Curious Story")
book.set_language("en")

# authors
book.add_author("R.R. Shrubber")
book.add_author(
    "The Knights",
    file_as="The Knights Who Say Ni",
    role="ill",
    uid="coauthor",
)

# chapters
c1 = epub.EpubHtml(title='Introduction',
                   file_name='intro.xhtml',
                   lang='en')
#c1.set_content(u'<html><body><h1>Introduction</h1><p>Introduction paragraph.</p></body></html>')
c1_content = BeautifulSoup(open("c1_content.html", encoding="utf8"), "html.parser")
c1.set_content(str(c1_content)) # needed to set html as string

c2 = epub.EpubHtml(title='About this book',
                   file_name='about.xhtml')
c2.set_content('<h1>About this book</h1><p>This is a book.</p>')

book.add_item(c1)
book.add_item(c2)

# styling
style = 'body { font-family: Times, Times New Roman, serif; }'

nav_css = epub.EpubItem(uid="style_nav",
                        file_name="style/nav.css",
                        media_type="text/css",
                        content=style)
book.add_item(nav_css)

# table of contents (ToC)
book.toc = (epub.Link('intro.xhtml', 'Introduction', 'intro'),
              (
                epub.Section('Languages'),
                (c1, c2)
              )
            )

book.spine = ['nav', c1, c2]

# add NCX and Navigation tile (?)
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# write
epub.write_epub('ebooklib_test.epub', book)


# read it?
book_readback = epub.read_epub('ebooklib_test.epub', {"ignore_ncx": True})
items = list(book_readback.get_items_of_type(ebooklib.ITEM_DOCUMENT))
print(items)
for item in book_readback.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print('==================================')
        print('NAME : ', item.get_name())
        print('----------------------------------')
        print(item.get_content())
        print('==================================')


#soup = BeautifulSoup(open("c1_content.html", encoding="utf8"), "html.parser")
#print(soup)