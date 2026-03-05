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
            result += f" {key}=\"{value}\""
        return result
        
    def __repr__(self):
        return (f"Node:\n"
                f"tag = {self.tag}\n"
                f"value = {self.value}\n"
                f"children = {self.children}\n"
                f"attributes ={self.props_to_html()}")

            
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        html_string = ("<" + self.tag + self.props_to_html() + ">" 
                       + self.value 
                       + "</" + self.tag + ">")
        return html_string
    
    def __repr__(self):
        return (f"Leafnode:\n"
                f"tag = {self.tag}\n"
                f"value = {self.value}\n"
                f"attributes ={self.props_to_html()}")


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError
        html_children = []
        for child in self.children:
            html_children.append(child.to_html())
        html_string = ("<" + self.tag + self.props_to_html() + ">" 
                       + "".join(html_children) 
                       + "</" + self.tag + ">")
        return html_string
    
    def __repr__(self):
        children_repr = "" 
    #    print(self.children)
        if self.children:
            for children in self.children:
                children_repr = children_repr + " ; " + children.value
        return (f"Parentnode:\n"
                f"tag = {self.tag}\n"f"attributes ={self.props_to_html()}"
                f"children ={children_repr}\n")


