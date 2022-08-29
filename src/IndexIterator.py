
class IndexIterator:
    # Generate an iterator with the data from self.traitFilesVariationsDictionary, from NFTCollection class
    def __init__(self, trait_files_variations_dictionary):
        self.maxValues = {}
        self.currentValues = {}

        for key in trait_files_variations_dictionary.keys():
            self.currentValues[key] = 0
            self.maxValues[key] = len(trait_files_variations_dictionary[key])

    def has_next(self):
        for key in self.currentValues.keys():
            if self.currentValues[key] != self.maxValues[key] - 1:
                return True
        return False

    def next(self):
        for key in self.maxValues.keys():
            if self.currentValues[key] == self.maxValues[key] - 1:
                self.currentValues[key] = 0
            else:
                self.currentValues[key] += 1
                break

    def __str__(self):
        return str(self.currentValues)
