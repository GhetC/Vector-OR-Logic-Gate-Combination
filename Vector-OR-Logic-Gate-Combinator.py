{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Inbal Help Combined.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "mount_file_id": "16bTdJbXBrifvGrKNVhXoFi1qYPYqakS1",
      "authorship_tag": "ABX9TyMoqP/dZ2JPlmSymgibFof8"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "#Inbal help combined"
      ],
      "metadata": {
        "id": "LMMxD9RdCN-Y"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gsqcW-QGCL8n",
        "outputId": "0d8221bc-3112-438e-8a63-9b54f8b58b1e"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Enter Path (without Quotation marks):\n",
            "/content/drive/MyDrive/eco test quads.xlsx\n",
            "Enter Path (without Quotation marks):\n",
            "/content/drive/MyDrive/eco test quads_output2.xlsx\n"
          ]
        }
      ],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from google.colab import files\n",
        "from google.colab import drive\n",
        "\n",
        "\n",
        "print (\"Enter Path (without Quotation marks):\")\n",
        "path=input()\n",
        "df=pd.read_excel(path)\n",
        "\n",
        "species_names = list(df.columns)\n",
        "df=df.to_numpy()\n",
        "\n",
        "cols=len(df[0,1:])\n",
        "rows=len(df[:,0])\n",
        "\n",
        "def pair_compare(row1,row2):       \n",
        "  comb_lst=([])\n",
        "  for i in range(cols):\n",
        "    if row1[i]==1 or row2[i]==1:\n",
        "     comb_lst=np.append(comb_lst, int(1))\n",
        "    else:\n",
        "      comb_lst=np.append(comb_lst, int(0))\n",
        "  comb_lst=comb_lst.reshape((cols,1))\n",
        "  return comb_lst.astype(int), int(sum(comb_lst))\n",
        "\n",
        "\n",
        "\n",
        "def Pairs_full_table(dataframe):\n",
        "  names_lst=([])\n",
        "  sums_lst=([])\n",
        "  pairs_matrix=np.full((cols,1),2,dtype=int)\n",
        "  for j in range(0, rows-1):\n",
        "    for i in range(j+1,rows):\n",
        "      overlap=False\n",
        "      row1_ints=[]\n",
        "      row2_ints=[]\n",
        "      pair_name=None\n",
        "\n",
        "      if type(dataframe[j,0])==str or type(dataframe[i,0])==str:\n",
        "        row1_ints=list(map(int, dataframe[j,0].split(\",\")))\n",
        "        row2_ints=list(map(int, dataframe[i,0].split(\",\")))\n",
        "\n",
        "      for x in row1_ints:\n",
        "        if x in row2_ints:\n",
        "          overlap=True\n",
        "          break\n",
        "\n",
        "      if overlap==True:\n",
        "        continue\n",
        "      \n",
        "      if row1_ints==[] or row2_ints==[]:\n",
        "        pair_name=str(dataframe[j,0])+\",\"+str(dataframe[i,0])\n",
        "      \n",
        "      if row1_ints!=[] or row2_ints!=[]:\n",
        "        comb_rows=row1_ints+row2_ints\n",
        "        comb_rows.sort()\n",
        "        pair_name=\",\".join(map(str, comb_rows))\n",
        "      \n",
        "      if pair_name in names_lst:\n",
        "        continue\n",
        "      \n",
        "      else:\n",
        "        names_lst=np.append(names_lst, pair_name)\n",
        "\n",
        "        P=pair_compare(dataframe[j,1:],dataframe[i,1:])\n",
        "        Tuple=[pair_name, P[1]]\n",
        "        sums_lst.append(Tuple)\n",
        "        if np.all(pairs_matrix==2):\n",
        "          pairs_matrix=P[0]\n",
        "        else:\n",
        "          pairs_matrix=np.concatenate((pairs_matrix,P[0]), axis=1)\n",
        "\n",
        "  return sums_lst, pairs_matrix.T\n",
        "\n",
        "\n",
        "Pairs=Pairs_full_table(df)\n",
        "\n",
        "index_names=[a[0] for a in Pairs[0]]\n",
        "Total_species=[a[1] for a in Pairs[0]]\n",
        "df1=pd.DataFrame(Pairs[1])\n",
        "df1.index = index_names\n",
        "df1.columns =species_names[1:]\n",
        "df1=df1.assign(Total=Total_species)\n",
        "df1\n",
        "print (\"Enter Path (without Quotation marks):\")\n",
        "out_path=input()\n",
        "with pd.ExcelWriter(out_path) as writer:\n",
        "    df1.to_excel(writer, \"Pairs\")  "
      ]
    }
  ]
}