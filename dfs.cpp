//DFS in a maze
#include<stdio.h>
#include <vector>
#include <iostream>
#include<gl/Gl.h>
#include<gl/glut.h>

using namespace std;

class GLinitPoint{
public:
    GLint x,y;
};

GLinitPoint CP;

void moveto(GLint x,GLint y){
    CP.x = x;
    CP.y = y;
}

void myInit(){
    glClearColor(1.0,1.0,1.0,0.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0,0.0,0.0);
    glPointSize(4.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-50.0,600.0,-50.0,580.0);
}

void lineto(GLint x,GLint y){
    glBegin(GL_LINES);
    glVertex2i(CP.x,CP.y);
    glVertex2i(x,y);
    glFlush();
    glEnd();
    CP.x = x;
    CP.y = y;
}

void drawDot(int x,int y){
    glBegin(GL_POINTS);
    glVertex2i(x,y);
    glEnd();
    glFlush();
}

vector<pair<int,int> > l;

void dfs(int r, int c,int food_r, int food_c, vector <string> grid){
    pair<int,int> it = l.back();
    int pacman_r = it.first;
    int pacman_c = it.second;
    l.pop_back();
    grid[pacman_r][pacman_c] = '1';
    if(grid[pacman_r -1][pacman_c] == '.' || grid[pacman_r + 1][pacman_c] == '.' || grid[pacman_r][pacman_c - 1] == '.' || grid[pacman_r][pacman_c + 1] == '.'){
        cout<<pacman_r<<" "<<pacman_c;
        drawDot(pacman_r*25,pacman_c*25);
        return;
    }
    if(grid[pacman_r - 1][pacman_c] == '-' && grid[pacman_r -1][pacman_c] != '1'){
        l.push_back(make_pair(pacman_r - 1,pacman_c));
    }
    if(grid[pacman_r][pacman_c - 1] == '-' && grid[pacman_r][pacman_c - 1] != '1'){
        l.push_back(make_pair(pacman_r,pacman_c - 1));
    }
    if(grid[pacman_r][pacman_c + 1] == '-' && grid[pacman_r][pacman_c + 1] != '1'){
        l.push_back(make_pair(pacman_r,pacman_c + 1));
    }
     if(grid[pacman_r + 1][pacman_c] == '-' && grid[pacman_r + 1][pacman_c] != '1'){
        l.push_back(make_pair(pacman_r + 1,pacman_c));
     }
     if(!l.empty()){
            for(int i=0;i<100000000;i++);
            drawDot(it.first*25,it.second*25);
            dfs(r,c,food_r,food_c,grid);
     }
}

void myDisplay(void){
    int r,c, pacman_r, pacman_c, food_r, food_c;
    r = 7;
    c = 20;
    pacman_r = 3;
    pacman_c = 9;
    moveto(3*25,9*25);
    glColor3f(1.0,0.0,0.0);
    drawDot(pacman_r*25,pacman_c*25);
    food_r = 1;
    food_c = 9;
    glColor3f(0.0,1.0,0.0);
    drawDot(food_r*25,food_c*25);
    glColor3f(0.0,0.0,1.0);
    vector <string> grid;

    for(int i=0; i<r; i++) {
        grid.push_back("%%%%%%%%%%%%%%%%%%%%");
        grid.push_back("%--------.-----%---%");
        grid.push_back("%-%%-%%-%%-%%-%%-%-%");
        grid.push_back("%--------P-------%-%");
        grid.push_back("%%%%%%%%%%%%%%%%%%-%");
        grid.push_back("%------------------%");
        grid.push_back("%%%%%%%%%%%%%%%%%%%% ");
    }
    glPointSize(24.0);

    for(int j=0;j<r;j++){
        for(int k=0;k<c;k++){
            if(grid[j][k] == '%'){
                drawDot(j*25,k*25);
            }
        }
    }
    glColor3f(0.0,0.0,0.0);
    glPointSize(4.0);
    l.push_back(make_pair(pacman_r,pacman_c));
    dfs( r, c, food_r, food_c, grid);
    cout<<"end";
    return;
}

int main(int argc,char** argv){
    glutInit(&argc,argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowPosition(100,150);
    glutInitWindowSize(600,580);
    glutCreateWindow("window");
    glutDisplayFunc(myDisplay);
    myInit();
    glutMainLoop();
    return 0;
}
