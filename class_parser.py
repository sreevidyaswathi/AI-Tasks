
import json
import pandas as pd
import numpy

json_file= open('bbox_labels_600_hierarchy.json','r')

# print(json_file)

data_json= json.loads(json_file.read())
# print(data_json)
json_file.close()


csv_data= pd.read_csv("oidv6-class-descriptions.csv")
# print(csv_data.info())

#All the siblings (the ones under the same parent) and parent class belongs to same Ancestor class(es)
Is_sib_parent_belong_sameAncestor=True

def getclassnames(labelnames):
    classnames=[]
    for i in labelnames:
        try:
            classnames.append(numpy.array(csv_data[csv_data["LabelName"]==i]["DisplayName"])[0])
        except: pass
    return classnames


def subcategory(label,subCateg,sibling_class,parent_class,ancestor_class):
    for cat in subCateg:
        # print(cat, list(cat.keys()))
        try:
            # print("hit")
            if(cat["LabelName"] == label):
                print("matched")
                for e in subCateg:
                   if(e["LabelName"]!=label):sibling_class.append(e["LabelName"])
                   else :pass
                
                if(ancestor_class!=[]): parent_class.append(ancestor_class.pop())
                else:parent_class.append(data_json["LabelName"])
                print(sibling_class,"Sibling")
                print(ancestor_class,"ancestor")  
                print(parent_class,"Parent")
                Siblingnames=getclassnames(sibling_class)
                Parentnames=getclassnames(parent_class)
                Ancestornames=getclassnames(ancestor_class)
                print(Siblingnames,"Sibling")
                print(Parentnames,"Parent")  
                print(Ancestornames,"Ancestor")
             
                break
                
            elif("Subcategory" in list(cat.keys()) ):
                    # print("Subcategory is present")
                    # subcategory = cat["Subcategory"] if("Subcategory" in list(cat.keys())) else cat["Part"]
                    ancestor_class.append(cat["LabelName"])
                    subcategory(label,cat["Subcategory"],sibling_class,parent_class,ancestor_class)
                    # print(ancestor_class,"Ancestor")
            else:
                    pass
            
        except Exception as e:
            print(e,"Exception", cat)
            pass

                        



def class_parser(cls_name):
    parent_class=[]
    sibling_class=[]
    ancestor_class=["/m/0bl9f"]
    label = numpy.array(csv_data[csv_data["DisplayName"]==cls_name]["LabelName"])[0]
    print(label)
    if(label==data_json["LabelName"]):
        parent_class.push(cls_name)
        sibling_class.push("no siblings")
        ancestor_class.push("no ancestors")
        Is_sib_parent_belong_sameAncestor = False
    else:
            try:
                # print(label, data_json["Subcategory"])
                subcategory(label,data_json["Subcategory"],sibling_class,parent_class,ancestor_class)
                

            except Exception as e:
                print(e)

    

class_parser("Washing machine")