
class PerfContext(object):
    def __init__(self, product_category, product, json_body=None):
        self.product_category = product_category
        self.projects = product['product']
        self.extra_key_values = json_body

    def get_context(self):
        output = {
            'category': self.product_category,
            'product': self.projects,
        }
        if self.extra_key_values:
            for key, value in self.extra_key_values.iteritems():
                output[key] = value
        return output
