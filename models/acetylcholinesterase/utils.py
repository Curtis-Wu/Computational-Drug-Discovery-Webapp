import pandas as pd
import subprocess
from chembl_webresource_client.new_client import new_client
import pickle

def model_predict(compounds_list):
    molecule = new_client.molecule
    my_res = []
    mols = molecule.filter(molecule_chembl_id__in=compounds_list).only(['molecule_chembl_id', 'molecule_structures'])
    for molecules in mols:
        my_res.append([molecules['molecule_structures']['canonical_smiles'],molecules['molecule_chembl_id']])


    df1 = pd.DataFrame(my_res,columns = ['Canonical Smiles','Molecule ChemBL ID'])
    df1.to_csv('molecule.smi', sep='\t', index=False, header=False)
    subprocess.run('models/acetylcholinesterase/padel.sh', shell=True, check = True) 
    df = pd.read_csv('models/acetylcholinesterase/data/descriptors_output.csv')
    
    df = df.drop(columns=['Name'])
    
    model = pickle.load(open("models/acetylcholinesterase/data/trained_model.pkl","rb"))
    features = pickle.load(open("models/acetylcholinesterase/data/selected_features.pkl","rb"))
    df = df[features]
    y_predicted = model.predict(df)

    b = [pow(10,-value)*1000000000 for value in y_predicted]
    df1['Predicted IC50 value (nM)'] = b

    return df1

if __name__ == '__main__':
    # testing purpose
    my_str = "CHEMBL133897 CHEMBL336398 CHEMBL336398"
    my_list = list(my_str.split(' '))
    res = model_predict(my_list)
    print(res)