class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f" {key}={value}"
        return result
        
    def __repr__(self):
        return (f"Node:\n"
                f"tag = {self.tag}\n"
                f"value = {self.value}\n"
                f"children = {self.children}\n"
                f"attributes ={self.props_to_html()}")
