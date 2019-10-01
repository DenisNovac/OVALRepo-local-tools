import re
# class with a recursive functions to parse xml
class RecursiveXMLSearcher:
    # private variables for recursion
    __one_tag = None
    __all_tags = [ ]

    # search one tag in xml-block and break
    def __search_one_tag( self, root, search ):
        # if tag is already found - exit
        if self.__one_tag:
            return self.__one_tag

        #print(root.tag)
        for tree_element in root:
            if re.search(search, tree_element.tag):
                #print('*'+tree_element.tag)
                self.__one_tag=tree_element
                return tree_element
            else:
                new_root = self.__search_one_tag(tree_element,search)
                # if managed to get minimal element - move tree_element
                if not new_root:
                    continue


    # search all tags in file (except for embedded tags)
    # if you want to search embedded tags - run this function again
    # with answer
    def __search_all_tags( self, root, search ):
        # print(root.tag)
        for tree_element in root:
            if re.search(search, tree_element.tag):
                # print('*'+tree_element.tag)
                self.__all_tags.append(tree_element)
                # we want to find all definitions so continue
                # and we'll never get to embedded search element this way
                continue
            else:
                self.__search_all_tags(tree_element, search)
        return

    # fancy functions-wrappers for private recursive functions
    def search_all( self, root, search ):
        self.__all_tags = [ ]
        self.__search_all_tags(root, search)
        return self.__all_tags

    def search_one( self, root, search ):
        self.__one_tag=None
        self.__search_one_tag(root, search)
        return self.__one_tag