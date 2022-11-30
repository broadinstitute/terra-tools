This workspace contains useful tools that may come in different flavors (Workflows, Notebooks, etc) you may need to perform some convenient Terra actions such as:

1. Remove intermediate files generated by your workflows
2. Update references in your Data Model if the location of your files changes   

Each section below contains:       
* Description of the tool
* How to implement the tool
* Notes and Considerations
 
---


## Jupyter Notebook : Remove_Workflow_Intermediates
#### **Disclaimer:** **This Notebook is to be implemented at the user’s discretion. We are not responsible for any unexpected behavior (user error or otherwise). Please ensure that you have saved the files you would like to persist to the Data Model (or a more permanent location)before running this Notebook.**

### **What is this Notebook?**
When launching large numbers of submissions, increased storage costs can be incurred due to accumulating intermediate output data. This notebook offers users a simple option to delete some of the workflow intermediates in a single Terra workspace's Google bucket.

### **What does it do?**
This Notebook utilizes the mop command from FISS, a programmatic interface to FireCloud that provides Python bindings to the API, to enable users to remove unwanted and/or unnecessary intermediate files. Outputs from a Workflow can include final products, like vcfs, as well as additional intermediate files from intermediate tasks. If intermediates are not necessary, storage in the bucket continually incurs a cost to the user. This option circumvents the need to manually delete intermediates in submissions and offers the option to keep required outputs.

### **How does it do it?**
Every submission launched (can contain single or multiple workflows) is assigned a submissionID that is used to label the “directory” in the Google bucket where output files are copied. With the individual workspace name and the Terra billing-project, a list of submissionIDs is generated and intermediate files within the submission directory are deleted.

### **Notes and Considerations**

**What gets deleted?**
Workflow output files minus logs are deleted except any outputs that are bound to the Data Model. To bind outputs to the Data Model, select Defaults from the Outputs section of the Workflow before selecting “Launch Analysis”.

**What gets left behind?**
* Files uploaded to the Google bucket that do not live inside a submission “directory” will NOT be deleted.
* Log files (stderr, stdout, .log) within a submission “directory” will NOT be deleted.
* Submission folders/“directories” will NOT be deleted - only the contents.
* Notebooks in the Google bucket will NOT be deleted.

**What should you do before using this Notebook?**
* If there are outputs that should not be deleted, they will need to be bound to the Data Model. If a file is NOT bound to the Data Model, it will be removed.
* If not bound to the Data Model, desired files should be copied to a secondary location.

### **To run this notebook**
1. Copy this Notebook into the workspace where you want to remove intermediates generated from launched submissions.
2. Open the Notebook and Create a Runtime Environment if necessary.
3. After the Notebook is open, select Cell > Run All.
4. You will be prompted to enter Yes/No before deletion begins. Enter Yes/No and press Enter.



-------

## Jupyter Notebook: Update_Data_Model_References
#### **Disclaimer:** **This Notebook is to be implemented at the user’s discretion. We are not responsible for any unexpected behavior (user error or otherwise). Please ensure that you have saved the your table .tsv files and/or data you would like to persist to a permanent location before running this Notebook.**

### **What is this Notebook?**
If a situation arises wherein a user must copy data from a current Google bucket to another, references in the Data Model pointing to the original location need to be updated. If many entities exist in a table, manual updates can be cumbersome and/or error prone. This Jupyter notebook can be used to programatically update the paths in your Data Model from existing gsutil source location to a new gsutil destination in a single Terra workspace.

### **What does it do?**
This Notebook utilizes Python code (hosted in GitHub) to call FireCloud APIs, enabling users to update paths in the Data Model from one gsutil bucket URL to a second gsutil bucket URL. This option circumvents manual updates of each entity in the Data Model should the data or reference paths change. 

### **How does it do it?**
The Python code allows the user to input the original Google bucket path (in String format) and the replacement Google bucket path (in String format). The Notebook interacts with the API to replace the original path with the new bucket paths.

### **Notes and Considerations**

**What gets updated?**
* The Notebook applies to all the entity tables in the Workspace including the Workspace References.

**What gets left behind?**
* Any entities that do not point to the original Google bucket gs:// URL will not be updated to the new gs:// URL.

**What should you do before using this Notebook?**
* If there are any important files that should be accessible, they will need to be saved to a secondary location. 

### **To run this notebook**
1. Copy this Notebook into the workspace where you want to update the Data Model references.
2. Open the Notebook and Create a Runtime Environment if necessary.
3. After the Notebook is open, select Cell > Run All.

-----

## Jupyter Notebook: Update_TCGA_Data_Model_DRS_URIs
#### **Disclaimer:** **This Notebook is to be implemented at the user’s discretion. We are not responsible for any unexpected behavior (user error or otherwise). Please ensure that you have saved the your table .tsv files and/or data you would like to persist to a permanent location before running this Notebook.**

### **What is this Notebook?**
Current TCGA data workspaces (open and controlled access) have data model tables with values that are string identifiers for the files in question. There is additional work required on the part of the user to resolve the UUID strings into formats that are ready to be used in Workflows. Running this notebook will update the tables, those that are applicable, with the new DRS 1.1 uri format that will no longer require any additional steps to access files. 

### **What does it do?**
This Notebook utilizes Python code to call FireCloud APIs, enabling users to update DRS uris in the Data Model from from string UUIDs to denote a file to a drs://dg.4DFC:UUID format.

### **How does it do it?**
The Python code allows the user to run the code in "dry-run" mode allowing them to first inspect potential changes. Then the user can switch the "dry-run" mode to `False` which will then re-run the code and update all the tables in the Data Model where relevant.

### **Notes and Considerations**

**What gets updated?**
* The Notebook applies to all the entity tables in the Workspace except tables of type, set. Set tables are not modified since they only reference the unique id of the entities in the entity table.

**What gets left behind?**
* Any entities that do not contain valid UUID formats or are in columns that are not defined to be updated.

**What should you do before using this Notebook?**
* Read the instructions in the Notebook to learn how to set the value of "dry-run" to `True` or `False` and to learn about what each option does.

### **To run this notebook**
1. Copy this Notebook into the workspace where you want to update the Data Model DRS uris.
2. Open the Notebook and Create a Runtime Environment if necessary.
3. After the Notebook is open, select Cell > Run All.

-----

## Jupyter Notebook: Get_Workflow_Metadata
#### **Disclaimer:** **This Notebook is to be implemented at the user’s discretion. We are not responsible for any unexpected behavior (user error or otherwise). Please ensure that you have saved the your table .tsv files and/or data you would like to persist to a permanent location before running this Notebook.**

### **What is this Notebook?**
When launching large numbers of submissions, it can be difficult to sort through the metadata of individual workflows. For example, agregating the costs of several hundred workflows requires clicking through each submission. This notebook offers users a simple option to fetch all or some of the workflow metadata, view it, and optionally export it to BigQuery.

### **What does it do?**
This notebook uses the Firecloud API to:

- List all the submissions of the current workspace.
- List all the workflows of a selected submission.
- For each workflow, parse out the cost, duration, and other metadata.


### **How does it do it?**
You may run step 1 of this notebook as-is. No modifications are necessary. Step 2 requires you to fill in the BigQuery IDs.

After running step 1 of this notebook, you will be prompted to select a `submissionId`. **Please copy and paste one from the displayed table, or type in "all" (without quotes) to pull all submissions**.




### **Notes and Considerations**

If your submission has several workflows, the notebook may take several minutes to run. This is because we must make one API call per workflow. For example, if your submission has 427 workflows, the notebook will make 427 sequential API calls which may take 4-6 minutes.

### **To run this notebook**
1. Copy this Notebook into the workspace that submitted the workflows.
2. Open the Notebook and Create a Runtime Environment if necessary.
3. After the Notebook is open, select Cell > Run All.


## Workspace Change Log
| Date | Change | Author |
| --- | --- | --- |
|  2020-02-18 | workspace created, dashboard updated, notebooks added | Sushma Chaluvadi |
|  2021-05-13 | drs uri notebook added, dashboard updated | Sushma Chaluvadi |
|  2022-10-28 | Get Workflow Data notebook added, dashboard updated | Willy Nojopranoto |

---

## Contact information  
For any questions, reach out to Terra-support@broadinstitute.zendesk.com or post on the [General Discussion forum](https://support.terra.bio/hc/en-us/community/topics/360000500432-General-Discussion).

---

## License  
**Copyright Broad Institute, 2019 | BSD-3**  
All code provided in this workspace is released under the WDL open source code license (BSD-3) (full license text at https://github.com/openwdl/wdl/blob/master/LICENSE). Note however that the programs called by the scripts may be subject to different licenses. Users are responsible for checking that they are authorized to run all programs before running these tools.