### usage
# googlesearch.search(str: term, int: num_results=10, str: lang="en") -> list
class Grants():
    """Google search grants results."""
    def get_search_results(self):
        from googlesearch import search
        ### limit language

        grants = search("bay area covid-19 business grants", num_results=100, lang="en")
        # print(grants)
        # print(len(grants))
        return grants



