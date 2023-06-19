class KeywordDependencyClass:
    pass


keyword_dependency_class_default_instance = KeywordDependencyClass()


class ClassWithKeywordDependencies:
    def __init__(self, keyword_dependency: KeywordDependencyClass = keyword_dependency_class_default_instance):
        self.keyword_dependency = keyword_dependency
