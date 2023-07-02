import numpy as np
import pickle
import os
import pandas as pd
from chembl_webresource_client.new_client import new_client

if __name__ == "__main__":
    my_str = "CHEMBL133897 CHEMBL336398"
    my_list = list(my_str.split(' '))
    #print(my_list)
    #my_array = np.array([my_list])
    #model = pickle.load(open("data/trained_model.pkl"),"rb")
    #os.popen('padel.sh')
    molecule = new_client.molecule
    selection = ['canonical_smiles','molecule_chembl_id']
    my_res = []
    mols = molecule.filter(molecule_chembl_id__in=my_list).only(['molecule_chembl_id', 'molecule_structures'])
    for molecule in mols:
        can = molecule['molecule_structures']['canonical_smiles']
        id = molecule['molecule_chembl_id']
        my_res.append([molecule['molecule_structures']['canonical_smiles'],molecule['molecule_chembl_id']])

    df = pd.DataFrame(my_res)
    df.to_csv('molecule.smi', sep='\t', index=False, header=False)
    print('overwritten')

    