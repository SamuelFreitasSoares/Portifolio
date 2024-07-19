import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_date, get_amount, get_category, get_description



class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"
    
    # método para inicializar um arquivo csv caso ele ja não exista
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    ## método para entrar com dados nas colunas do arquivo csv
    # abre o csv no modo append
    # o with é um gerenciador de contexto, ele garante que o arquivo será fechado sem memory leak
    # além de garantir que o formato do arquivo será csv
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description} # dicionario com os valores a serem adicionados
        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) # fieldname associa as colunas do csv com as keys do dicionario
            writer.writerow(new_entry) # escreve na row com os dados obtidos no dicionario
        print("Entry added successfully!")
            
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # converter todas as datas da coluna 'date' para um objeto datetime
        # strptime = parse uma string para um objeto datetime
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        #filtro para ver se a data selecionada está entre o start_date e o end_date
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        # retorna o dataframe filtrado pela mask usando a função loc
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print("No transactions found for the selected period")
        else:
            # {converte para string de novo para printar}
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            # formatters = formata a data para o formato especificado atraves da função lambda onde x será a data recebida e formatada
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            # soma o total de income e expense das datas filtradas 
            # ela filtra o dataframe onde a categoria é igual a "Income" e soma os valores da coluna "amount"
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum() 
            print("\nSummary: ")
            # printa arredondando pra 2 casas decimais
            print(f"Total Income: ${total_income:0.2f}")
            print(f"Total Expense: ${total_expense:0.2f}")
            print(f"Net savings: ${(total_income - total_expense):0.2f}")
        return filtered_df
            
        
        
        
# função para adicionar uma entrada no csv
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (dd-mm-yyyy) or press 'Enter' to use today's date: ",
                    allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()         
    CSV.add_entry(date, amount, category, description)       

def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. add new transaction")
        print("\n2. view transactions and summary within a date range")
        print("\n3. exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3")
            
# se o nome do arquivo for main ele executa a função main :)           
if __name__ == "__main__":
    main()