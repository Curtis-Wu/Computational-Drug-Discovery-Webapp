from chembl_webresource_client.new_client import new_client
import pandas as pd
import subprocess
import lightgbm as lgb
import pickle
import os
from keras.models import load_model

def model_predict(compound_name,compounds_str,id):
    compounds_list = list(compounds_str.split(' '))
    print(f"compounds_list is {compounds_list}")
    molecule = new_client.molecule
    my_res = []
    mols = molecule.filter(molecule_chembl_id__in=compounds_list).only(['molecule_chembl_id', 'molecule_structures'])
    for molecules in mols:
        my_res.append([molecules['molecule_structures']['canonical_smiles'],molecules['molecule_chembl_id']])

    
    file_id = compound_name+'_'+id
    print(f"file_id is {file_id}")
    filename = file_id + '.smi'
    print(f"file_name is {filename}")
    df1 = pd.DataFrame(my_res,columns = ['Canonical Smiles','Molecule ChemBL ID'])
    df1.to_csv(filename, sep='\t', index=False, header=False)
    filepath = 'models/'+compound_name
    
    subprocess.run(f'models/acetylcholinesterase/padel.sh {filename}', shell=True, check=True)
    df = pd.read_csv(file_id+'_descriptors_output.csv')
    #subprocess.run('models/acetylcholinesterase/padel.sh', shell=True, check = True) 
    #df = pd.read_csv('models/acetylcholinesterase/data/descriptors_output.csv')
    os.remove(os.path.abspath(filename))
    os.remove(os.path.abspath(file_id+'_descriptors_output.csv'))

    print("successfully read df")
    df = df.drop(columns=['Name'])
    print("successfully dropped column")
    features = pickle.load(open((filepath+"/data/selected_features.pkl"),"rb"))
    df = df[features]
    print(f"datafram is {df}")
    
    if df.empty:
        return df
    
    if compound_name == 'vegfr2':
        model = load_model((filepath+'/data/my_model.h5'))
    elif compound_name == "hiv1rt":
        model = pickle.load(open((filepath+"/data/trained_model.pkl"),"rb"))
    else:
        model = lgb.Booster(model_file=filepath+'data/trained_model.txt')

    y_predicted = model.predict(df)
    b = [pow(10,-value)*1000000000 for value in y_predicted]
    df1['Predicted IC50 value (nM)'] = b

    print(df1)

    return df1

if __name__ == '__main__':
    # testing purpose
    my_str = "CHEMBL133897 CHEMBL336398 CHEMBL336398"
    my_list = list(my_str.split(' '))
    res = model_predict(my_list)
    print(res)