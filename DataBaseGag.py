import sqlite3 as sql
#IMPORTANT ---> WE HAVE TO BE IN THE RIGHT FOLDER TO CREATE THE DATABASE 
#BECAUSE THE OTHERS SCRIPTS WILL READ THE DATABASE FROM ITS OWN FOLDER

FILE_DATABASE = "AxionsGag.db"
PATH_DATA = "data/axion/"

#CREATES THE DATABASE (JUST 1 TIME UNLESS LOTS OF DATA NEED TO BE UPDATED)
#CreateDB()
def CreateDB():
    conn = sql.connect(FILE_DATABASE)
    conn.commit()
    conn.close()


#CREATES THE TABLE OF THE DATABASE IS THE INTERFACE OF THE DATABASE 
#(ASWELL IT NEEDS TO BE CREATED ONCE UNLESS LOTS OF DATA NEEDS TO BE UPDATED)
#CreataTable
def CreateTable():
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Axions (
        name text , 
        type text ,
        path text ,
        noPlotType integer,
        large_panorama integer,
        panorama integer,
        helioscopes integer,
        haloscopes integer,
        lswexps integer,
        projection integer
        )"""
    )
    conn.commit()
    conn.close()
    

#Use to insert one row at a time
#for  example we wnat to introduce a new experiment that appear in panorama and LSWexp
# called new_exp with th type band and it's not a projection
#InsterRow('new_exp',band,0,0,1,0,0,1,0)
def InsertRow(name, type, path, noPT=1, LP=0, P=0, Helios=0, Halos=0, LSW=0 ,projection=0): #PARA AÑADIR UNA SOLA COLUMNA (IDEAL PARA AÑADIR UN EXPERIMENTO NUEVO)
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Axions  VALUES ('{name}', '{type}','{path}','{noPT}','{LP}','{P}','{Helios}','{Halos}',{LSW},{projection})"
    cursor.execute(instruction)
    conn.commit()
    conn.close()    


#Use for read all data without ccriteria
#data = ReadRows()
def ReadRows(): 
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions"
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close() 
    print(data)

#Use for inster multiple rows in the form of a list os list with all the parameters and separeted by commas
#
def InsertRows(axionexps): #ESTA ES PARECIDA A LA DE UNA SOLA COLUMNA PERO AÑADIENDO MAS PARA ELLO HAY QUE DEFINIR UNA LISTA DE LISTAS CON LOS EXPERIMENTOS COMO ESTA HECHO MAS ADELANTE
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Axions  VALUES (?,?,?,?,?,?,?,?,?,?)"
    cursor.executemany(instruction,axionexps)
    conn.commit()
    conn.close()


def ReadOrdered(field): #SE USA PARA LEER LA LISTA Y QUE DEVUELVA UN LISTA ORDENADA SEGUN UN CRITERIO
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    #Se lee ordenado alfabeticamente, y de menor a mayor , para la inversa escribir DESC despues de {field}
    instruction = f"SELECT * FROM Axions ORDER BY {field}"
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close() 
    print(data)


#Use for searching all the data that validate the requesst such as i want all data that appears in panorama (panorama token = 1)
#data = search('panorama',1)
def Search(field, token): 
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions WHERE {field} = {token} "
    cursor.execute(instruction)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


#Use for searching the names that validate the request such as i want all the name where the token for panorama is 1
# names = search_names('panorama',1)
def Search_Names(field, token):
    names = []
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"SELECT * FROM Axions WHERE {field} = {token} "
    cursor.execute(instruction)
    data = cursor.fetchall()
    for row in data:
        names.append(row[0])
    conn.commit()
    conn.close()
    return names


#Use for update one value for 1 row such as modifie in qcdband the parameter panorama with value 1 update('qcdband','panorama',1)
#Now the token for panorama for the name qcdband is 1 so it will appear in the panorama plot
def Update(name,field,value): #SE USA PARA MODIFICAR UN ELEMENTO 
    conn = sql.connect(FILE_DATABASE)
    cursor = conn.cursor()
    instruction = f"UPDATE Axions SET '{field}' == {value} WHERE name ='{name}'"
    cursor.execute(instruction)

    conn.commit()
    conn.close() 


#Use for deleting a row with its name such as if i want to delete the qcdband
#deleteRow('qcdband')
def DeleteRow(name): #PARA ELIMINAR UNA FILA
    conn = sql.connect(FILE_DATABASE)

    cursor = conn.cursor()
    instruction = f"DELETE FROM Axions WHERE name = '{name}' "
    cursor.execute(instruction)
    conn.commit()
    conn.close() 

#InsertRow("name","band",PATH_DATA + "/name.dat",Large_Panorama,Panaroma,Helios,Halos,LSW,Projection)
#ReadRows()
axionsexps= [
    ["qcdband", "band", PATH_DATA + "QCD_band.dat", 1, 1, 1, 1, 1, 1, 0],
    ["ksvz", "region", PATH_DATA + "ksvz.dat", 1, 1, 1, 1, 1, 1, 0],
    ["dfsz", "region", PATH_DATA + "dfsz.dat", 0, 0, 1, 0, 0, 0, 0],
    ["ADMX2018", "band", PATH_DATA + "ADMX2018.txt", 1, 1, 1, 1, 1, 0, 0],
    ["ADMX2019", "band", PATH_DATA + "ADMX2019.dat", 1, 1, 1, 1, 1, 0, 0],
    ["ADMX2019_1", "band", PATH_DATA + "ADMX2019_1.txt", 0, 0, 0, 0, 0, 0, 0],
    ["ADMX2019_2", "band", PATH_DATA + "ADMX2019_2.txt", 0, 0, 0, 0, 0, 0, 0],
    ["ADMX2021", "band", PATH_DATA + "ADMX2021.txt", 1, 1, 1, 1, 1, 0, 0],
    ["ADMX_sidecar", "band", PATH_DATA + "ADMX_sidecar.txt", 1, 1, 1, 1, 1, 0, 0],
    ["admx", "band", PATH_DATA + "admx.txt", 1, 1, 1, 1, 1, 0, 0],
    ["admx_hf_2016", "band", PATH_DATA + "admx_hf_2016.dat", 1, 1, 1, 1, 0, 0, 0],
    ["CAPP-8TB", "band", PATH_DATA + "CAPP-8TB.txt", 1, 1, 1, 1, 1, 0, 0],
    ["CAPP_multicell", "band", PATH_DATA + "CAPP_multicell_2020.dat", 0, 0, 0, 0, 1, 0, 0],
    ["CAPP2021", "band", PATH_DATA + "CAPP2021.txt", 0, 0, 1, 0, 1, 0, 0],
    ["HAYSTAC", "band", PATH_DATA + "HAYSTAC.txt", 1, 1, 1, 1, 1, 0, 0],
    ["HAYSTAC2020", "band", PATH_DATA + "haystac2020.txt", 1, 1, 1, 1, 1, 0, 0],
    ["ORGAN", "band", PATH_DATA + "ORGAN.txt", 1, 1, 1, 1, 1, 0, 0],
    ["QUAX", "band", PATH_DATA + "QUAX.txt", 1, 1, 1, 1, 1, 0, 0],
    ["QUAX2021", "band", PATH_DATA + "QUAX2021.txt", 1, 1, 1, 1, 1, 0, 0],
    ["RADES2021", "band", PATH_DATA + "RADES2021.txt", 1, 1, 1, 1, 1, 0, 0],
    ["THintMayer", "region", PATH_DATA + "Mayer_2013.dat", 0, 0, 0, 1, 0, 1, 1],
    ["THintCIBER", "region", PATH_DATA + "CIBER_contour_data.dat", 0, 0, 0, 0, 0, 1, 1],
    ["HBhint", "region", PATH_DATA + "hints/HB_hint.dat", 0, 0, 0, 1, 0, 1, 1],
    ["ABRA10cm", "band", PATH_DATA + "ABRA10cm.txt", 0, 0, 0, 0, 0, 0, 0],
    ["BASE_2021", "band", PATH_DATA + "BASE2021.txt", 0, 0, 0, 1, 0, 0, 0],
    ["ADMX_SLIC", "band", PATH_DATA + "ADMX_SLIC.txt", 1, 1, 1, 1, 1, 0, 0],
    ["hess", "band", PATH_DATA + "hess.dat", 1, 1, 1, 1, 0, 1, 0],
    ["mrk421", "band", PATH_DATA + "Mrk421.txt", 1, 1, 1, 1, 0, 1, 0],
    ["sn1987a_photon", "band", PATH_DATA + "sn1987a_photon.dat", 1, 1, 1, 1, 0, 1, 0],
    ["FERMI_NG1275", "region", PATH_DATA + "FERMI_NG1275_region.dat", 1, 1, 1, 1, 0, 1, 0],
    ["SN1987energyloss", "band", PATH_DATA + "cosmoalp/SN1987energyloss.txt", 1, 1, 0, 0, 0, 0, 0],
    ["Xray", "band", PATH_DATA + "cosmoalp/Xray.txt", 1, 1, 0, 0, 0, 0, 0],
    ["Deut2016", "region", PATH_DATA + "cosmoalp/Deut2016.txt", 1, 1, 0, 0, 0, 0, 0],
    ["OpticalDepthTerm", "band", PATH_DATA + "cosmoalp/OpticalDepthTerm.txt", 1, 1, 0, 0, 0, 0, 0],
    ["gEBL1", "band", PATH_DATA + "cosmoalp/gEBL1.txt", 1, 1, 0, 0, 0, 0, 0],
    ["EBL2", "region", PATH_DATA + "cosmoalp/EBL2.txt", 1, 1, 0, 0, 0, 0, 0],
    ["cmb_mu", "region", PATH_DATA + "cosmoalp/CMB_mu.txt", 1, 1, 0, 0, 0, 0, 0],
    ["CMB_DEsuE", "band", PATH_DATA + "cosmoalp/CMB_DEsuE.txt", 0, 0, 0, 0, 0, 0, 0],
    ["Overduin", "region", PATH_DATA + "cosmoalp/Overduin.txt", 1, 1, 0, 0, 0, 0, 0],
    ["Ressell", "band", PATH_DATA + "cosmoalp/Ressell.txt", 1, 1, 0, 0, 0, 0, 0],
    ["endlist2_gamma_projimprov", "band", PATH_DATA + "endlist2_gamma_projimprov.txt", 1, 1, 1, 1, 0, 0, 0],
    ["HBalpbound", "band", PATH_DATA + "HBalpbound.txt", 1, 1, 0, 0, 0, 0, 0],
    ["HBalpbound_l", "line", PATH_DATA + "HBalpbound.txt", 0, 0, 1, 1, 0, 0, 0],
    ["telescopes", "band", PATH_DATA + "telescopes.dat", 1, 1, 1, 1, 0, 0, 0],
    ["telescopes_new", "band", PATH_DATA + "telescopes_new.dat", 1, 1, 1, 1, 0, 0, 0],
    ["solar_nu", "band", PATH_DATA + "ALPSun_nu.txt", 1, 1, 1, 1, 0, 0, 0],
    ["ADMXprosp_2GHz", "band", PATH_DATA + "ADMX_prospects_2GHz.dat", 1, 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_10GHz", "band", PATH_DATA + "ADMX_prospects_10GHz.dat", 1, 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_2GHz_l", "line", PATH_DATA + "ADMX_prospects_2GHz.dat", 1, 1, 1, 0, 1, 0, 1],
    ["ADMXprosp_10GHz_l", "line", PATH_DATA + "ADMX_prospects_10GHz.dat", 1, 1, 1, 0, 1, 0, 1],
    ["CAPP4", "line", PATH_DATA + "CAPP4.dat", 0, 0, 1, 0, 0, 0, 1],
    ["MADMAX", "band", PATH_DATA + "MADMAX.dat", 0, 0, 1, 0, 0, 0, 1],
    ["CAPP4_l", "line", PATH_DATA + "CAPP4.dat", 1, 1, 0, 0, 1, 0, 1],
    ["MADMAX_l", "line", PATH_DATA + "MADMAX.dat", 1, 1, 1, 0, 1, 0, 1],
    ["ORGANprosp", "line", PATH_DATA + "ORGAN2.dat", 1, 1, 1, 0, 1, 0, 1],
    ["castcapp2", "band", PATH_DATA + "CASTCAPP2.dat", 0, 0, 1, 0, 0, 0, 1],
    ["ABRA1", "band", PATH_DATA + "ABRAres_1.dat", 1, 1, 1, 0, 1, 0, 1],
    ["ABRA1_l", "line", PATH_DATA + "ABRAres_1.dat", 1, 1, 0, 0, 0, 0, 1],
    ["ABRA2", "line", PATH_DATA + "ABRAres_2.dat", 0, 0, 0, 0, 1, 0, 1],
    ["ABRA3", "line", PATH_DATA + "ABRAres_3.dat", 0, 0, 0, 0, 1, 0, 1],
    ["ABRA1_l", "line", PATH_DATA + "ABRAres_1.dat", 1, 1, 0, 0, 0, 0, 1],
    ["ABRA_2021_l", "line", PATH_DATA + "ABRA_2021.txt", 0, 0, 0, 0, 0, 0, 1],
    ["KLASH", "line", PATH_DATA + "KLASH.dat", 0, 0, 1, 0, 1, 0, 1],
    ["old_haloscopes", "band", PATH_DATA + "MicrowaveCavities.txt", 1, 1, 1, 1, 1, 0, 0],
    ["IAXODM", "band", PATH_DATA + "IAXODM.dat", 0, 0, 1, 0, 0, 0, 1],
    ["IAXODM_l", "line", PATH_DATA + "ORGAN2.dat", 0, 0, 1, 0, 0, 0, 1],
    ["CAST", "band", PATH_DATA + "cast_env_2016.dat", 1, 1, 1, 1, 1, 1, 0],
    ["SHAFT", "band", PATH_DATA + "SHAFT.txt", 0, 0, 1, 1, 0, 0, 0],
    ["ABRA_2021", "band", PATH_DATA + "ABRA_2021.txt", 0, 0, 1, 1, 0, 0, 0],
    ["BabyIAXO", "band", PATH_DATA + "miniIAXO.dat", 1, 1, 1, 1, 1, 0, 1],
    ["IAXO", "band", PATH_DATA + "IAXO_nominal.txt", 0, 0, 1, 1, 1, 0, 1],
    ["IAXOplus", "band", PATH_DATA + "IAXO_plus.txt", 1, 1, 1, 1, 1, 0, 1],
    ["ALPSII", "band", PATH_DATA + "ALPSII.dat", 1, 1, 0, 1, 0, 1, 1],
    ["TOORAD", "line", PATH_DATA + "TOORAD2.txt", 0, 0, 0, 0, 1, 0, 1],
    ["BRASS", "line", PATH_DATA + "BRASS.txt", 0, 0, 0, 0, 1, 0, 1],
    ["STAX1", "line", PATH_DATA + "STAX1.dat", 0, 0, 0, 0, 0, 1, 1],
    ["STAX2", "line", PATH_DATA + "STAX2.dat", 0, 0, 0, 0, 0, 1, 1],
    ["BabyIAXO_l", "line", PATH_DATA + "miniIAXO.dat", 1, 1, 1, 1, 1, 0, 1],
    ["IAXO_l", "line", PATH_DATA + "IAXO_nominal.txt", 0, 0, 1, 1, 1, 0, 1],
    ["IAXOplus_l", "line", PATH_DATA + "IAXO_plus.txt", 1, 1, 1, 1, 1, 0, 1],
    ["ALPSII_l", "line", PATH_DATA + "ALPSII.dat", 1, 1, 1, 1, 0, 0, 1],
    ["KLASH_l", "line", PATH_DATA + "KLASH.dat", 0, 0, 0, 0, 0, 0, 1],
    ["AMELIE", "line", PATH_DATA + "amelie_1m3_arXiv_1508.03006.txt", 0, 0, 0, 1, 0, 0, 1],
    ["JURA", "line", PATH_DATA + "ALPSIII.dat", 0, 0, 0, 0, 0, 1, 1],
    ["OSCAR2015", "band", PATH_DATA + "osqar2015.dat", 1, 1, 1, 1, 0, 1, 0],
    ["PVLAS2015", "band", PATH_DATA + "pvlas2015.dat", 1, 1, 1, 1, 0, 1, 0],
    ["ALPSI", "band", PATH_DATA + "ALPSI.dat", 0, 0, 1, 1, 0, 1, 0],
    ["CROWS", "band", PATH_DATA + "CROWS.txt", 1, 1, 0, 0, 0, 1, 0],
    ["BeamDump", "region", PATH_DATA + "llSLAC137.txt", 1, 1, 0, 0, 0, 0, 0]]
#CreateDB()
#RreateTable()
#InsertRows(axionsexps)
#ReadOrdered("name")
data=Search("large_panorama",1) #devuelve una lista de lista con los elementos buscados
#print(data)

name = Search_Names("large_panorama",1)
#print(name)
#print(names)
#
#deleteRow()
#for name in names:
    #print(name)
