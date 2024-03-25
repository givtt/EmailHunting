import re


class Helper:

    def clean_input(self, _input):
        if type(_input) is int or type(_input) is bool:
            return _input

        sql_pattern = r'\'|\"|;|--'
        input_string = re.sub(sql_pattern, '', _input, flags=re.IGNORECASE)
        input_string = re.sub(r'<.*?>', '', input_string)
        input_string = re.sub(r'javascript:|on\w+=', '', input_string, flags=re.IGNORECASE)
        input_string = re.sub(r'[!#$%^&*()+=]', '', input_string)
        if "@" in input_string and input_string[0] == "@":
            input_string = input_string[:1]

        input_string = input_string.lower()
        input_string = ' '.join(input_string.split())
        input_string = input_string.strip()
        input_string = input_string.replace(" ", "")
        return input_string