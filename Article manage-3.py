import logging
import re

class ArticleManager:
    def __init__(self, article_text, options):
        """
        Initializes the ArticleManager with the given article text and options.

        :param article_text: The content of the article (string).
        :param options: A dictionary containing the following keys:
            - 'words_per_line' (int): Number of words per line.
            - 'lines_per_page' (int): Number of lines per page.
            - 'payment_structure' (dict): A dictionary defining payment ranges and amounts.
        """
        self.article_text = article_text
        self.words_per_line = options.get('words_per_line', 12)
        self.lines_per_page = options.get('lines_per_page', 20)
        self.payment_structure = options.get('payment_structure', {
            (0, 0): 0,       # Payment for fewer than one page
            (1, 2): 30,      # Payment for 1-2 pages
            (3, 4): 60,      # Payment for 3-4 pages
            (5, float('inf')): 100  # Payment for 5+ pages
        })

        # Set up logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def split_article(self):
        """
        A generator that splits the article into pages and lines while minimizing memory usage.

        :return: Yields pages, each containing a list of strings (lines).
        """
        if not isinstance(self.article_text, str):
            raise ValueError("Article text must be a string.")

        words = self.article_text.split()
        total_words = len(words)
        lines = (words[i:i + self.words_per_line] for i in range(0, total_words, self.words_per_line))

        page = []
        for line in lines:
            page.append(" ".join(line))  # Join words into a single line string
            if len(page) == self.lines_per_page:
                yield page  # Yield a full page
                page = []  # Reset for the next page

        # Yield any remaining lines as the final partial page
        if page:
            yield page

    def calculate_payment(self, num_pages, total_words):
        """
        Calculates payment based on the number of pages, including partial pages.

        :param num_pages: The number of full pages.
        :param total_words: The total number of words in the article.
        :return: The payment amount.
        """
        # Account for partial pages
        full_pages = num_pages
        partial_page = 1 if (total_words % (self.words_per_line * self.lines_per_page)) > 0 else 0

        # Total pages include full pages and one partial page if applicable
        total_pages = full_pages + partial_page

        # Apply payment structure
        for page_range, payment in self.payment_structure.items():
            if page_range[0] <= total_pages <= page_range[1]:
                return payment

        return 0

    def process_article(self):
        """
        Processes the article by splitting it into pages, calculating payment,
        and displaying the output.

        :return: None
        """
        try:
            pages = list(self.split_article())  # Collect all pages from the generator
            num_pages = len(pages)
            total_words = len(self.article_text.split())
            payment = self.calculate_payment(num_pages, total_words)

            # Display output
            print(f"Total Pages: {num_pages}")
            print(f"Payment Due: ${payment}")

            for idx, page in enumerate(pages, start=1):
                page_content = "\n".join(page)  # Join lines into page content
                print(f"Page {idx}:")
                print(page_content)

        except ValueError as e:
            logging.error(f"Error processing article: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Example usage
    article_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    # Define options dictionary
    options = {
        'words_per_line': 12,  # Number of words per line
        'lines_per_page': 20,  # Number of lines per page
        'payment_structure': {
            (0, 0): 0,       # Payment for fewer than one page
            (1, 2): 30,      # Payment for 1-2 pages
            (3, 4): 60,      # Payment for 3-4 pages
            (5, float('inf')): 100  # Payment for 5+ pages
        }
    }

    # Create an instance of ArticleManager
    article_manager = ArticleManager(article_text, options)

    # Process the article
    article_manager.process_article()

