#include<iostream>
#include<vector>
#include<fstream>
#include<sstream>
#include<cassert>
using namespace std;

struct Box{
    double lx,ly,rx,ry;
};

void getLeftRoi(const string& file,vector<Box> &originalRoi){
    ifstream infile;
    infile.open(file.data());
    // assert(infile.is_open());
    string line;
    while(getline(infile,line)){
        istringstream iss(line);
        Box box;
        iss >> box.lx >> box.ly >> box.rx >> box.ry;
        originalRoi.push_back(box);
    }
    infile.close();
    for(Box box: originalRoi){
        cout << box.lx << ","<< box.ly << "," << box.rx << "," << box.ry<< endl;
    }
}


vector<Box> get_hand_roi(const double bedDist,const string& filePath){
    vector<Box> originalRoi;
    getLeftRoi(filePath,originalRoi);
    assert(originalRoi.size() == 2);
    // cout << "roi size:" << originalRoi.size() << endl;
    double pixDist = bedDist * 400;  //10cm --> 40pix

    for (int i = 0; i<originalRoi.size(); i++) {
        originalRoi[i].lx += pixDist;
        originalRoi[i].rx += pixDist;
    }
    return originalRoi;
}



int main(void){
    string file = "./roi.txt";
    double bedDist = 0.10;

    vector<Box> originalRoi;
    originalRoi = get_hand_roi(bedDist,file);
    for(Box box: originalRoi){
        cout << box.lx << ","<< box.ly << "," << box.rx << "," << box.ry << endl;
    }
}