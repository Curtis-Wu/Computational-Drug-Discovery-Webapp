import pandas as pd
import subprocess
from chembl_webresource_client.new_client import new_client
import pickle
from keras.models import load_model

def model_predict(compound_name,compounds_str):
    compounds_list = list(compounds_str.split(' '))
    print(f"compounds_list is {compounds_list}")
    molecule = new_client.molecule
    my_res = []
    mols = molecule.filter(molecule_chembl_id__in=compounds_list).only(['molecule_chembl_id', 'molecule_structures'])
    for molecules in mols:
        my_res.append([molecules['molecule_structures']['canonical_smiles'],molecules['molecule_chembl_id']])
    
    df1 = pd.DataFrame(my_res,columns = ['Canonical Smiles','Molecule ChemBL ID'])
    df1.to_csv('molecule.smi', sep='\t', index=False, header=False)
    filepath = 'models/'+compound_name

    subprocess.run('models/acetylcholinesterase/padel.sh', shell=True, check = True) 
    df = pd.read_csv('models/acetylcholinesterase/data/descriptors_output.csv')
    
    df = df.drop(columns=['Name'])
    features = pickle.load(open((filepath+"/data/selected_features.pkl"),"rb"))
    df = df[features]
    print(f"datafram is {df}")

    if compound_name == 'vegfr2':
        model = load_model((filepath+'/data/my_model.h5'))
    else:
        model = pickle.load(open((filepath+"/data/trained_model.pkl"),"rb"))

    y_predicted = model.predict(df)
    b = [pow(10,-value)*1000000000 for value in y_predicted]
    df1['Predicted IC50 value (nM)'] = b

    print(df1)

    return df1

# def create_model_instance(compound_name, filename=None, data=None):

#     from app import mol_acetylcho, mol_vegfr2, mol_bace1

#     model_map = {
#         "acetylcholinesterase": mol_acetylcho,
#         "vegfr2": mol_vegfr2,
#         "bace1": mol_bace1,
#     }

#     if compound_name not in model_map:
#         raise ValueError(f"Invalid compound name: {compound_name}")

#     model_class = model_map[compound_name]
#     upload = model_class(filename=filename, data=data)
#     return upload

if __name__ == '__main__':
    # testing purpose
    my_str = "CHEMBL133897 CHEMBL336398 CHEMBL336398"
    my_list = list(my_str.split(' '))
    res = model_predict(my_list)
    print(res)