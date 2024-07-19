from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income","E":"Expense"}

# função recursiva para pegar a data
# o prompt é o que será inserido pelo usuário antes da data
# o allow_default deixa o usuario selecionar a data atual por padrao sem ter que inserí-la
def get_date(prompt,allow_default=False):
    date_str = input(prompt)
    
    # se allow for True e o usuário não inserir nada, a data atual será retornada
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    # se a data inserida não estiver no formato correto, a função tenta corrigi-la
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    
    # se não conseguir corrigir, a função retorna um erro e pede que o usuário insira a data no formato correto dd-mm-yyyy
    except ValueError:
        print("Invalid date format. Please insert a date in the format dd-mm-yyyy")
        return get_date(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount

    except ValueError as e:
        print(e)
        return get_amount()
        

def get_category():
    category = input("Enter the category ('I' - income || 'E' - expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category. Please enter 'I' for income or 'E' for expense")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")