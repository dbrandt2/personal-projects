//This will be the main file for my C++ OpenGL conways game of life project

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <GLFW/glfw3.h>
#include <thread>
#include <chrono>

using namespace std;


//define a square class here, this will store
class Square
{
public:
    //constructor
    Square()
    {
        m_isDead = true;
    }

    //getters and setters
    void setIsDead(bool isDead)
    {
        m_isDead = isDead;
    }

    bool getIsDead()
    {
        return m_isDead;
    }

    void setCol(int col)
    {
        m_col = col;
    }

    int getCol()
    {
        return m_col;
    }

    void setRow(int row)
    {
        m_row = row;
    }

    int getRow()
    {
        return m_row;
    }

    float getSize()
    {
        return m_size;
    }

    void drawSquare(int i, int j)
    {
        int windowOffset = 1; //this will make the draw start from the bottom left of the window, these can be modified in the x and the y direction to change the drawing start position
        if (m_isDead)
        {
            glColor3f(0.0f, 0.0f, 0.0f);
        }
        else
        {
            glColor3f(.220f, .20f, .60f);
        }
        glRectf((m_size * i) - windowOffset, (m_size * j) - windowOffset, ((i + 1) * m_size) - windowOffset, ((j + 1) * m_size) - windowOffset);
    }

    int checkNeighbors(Square** grid, int actualGridSize)
    {
        int gridSize = actualGridSize - 1; // this is because we start counting at 0 when making the grid so the outer elements of the grid are actually the gridSize - 1
        int aliveNeighbors = 0;
        if (m_col != 0 && m_row != 0 && m_col != gridSize && m_row != gridSize)  //cell is not an edge cell
        {
            for (int i = m_col - 1; i <= m_col + 1; i++)
                for (int j = m_row - 1; j <= m_row + 1; j++)
                    if (!grid[i][j].m_isDead)// && i != m_col && j != m_row)
                    {
                        aliveNeighbors++;
                    }

            // The cell needs to be subtracted 
            // from its neighbours as it was  
            // counted before 
           // aliveNeighbors--; //TODO: why does having this off get something to display
        }
        //else if (m_col == 0 && (m_row != 0 || m_row != gridSize)) //cell is left edge and not top left or bottom left
        //{
        //    for (int i = m_col; i < m_col + 1; i++)
        //    {
        //        for(int j = m_row + 1; j < m_row - 1; j--)
        //        {
        //            if (!grid[i][j].m_isDead)
        //            {
        //                aliveNeighbors++;
        //            }
        //        }
        //    }
        //}
        //else if (m_col == gridSize && (m_row != 0 || m_row != gridSize)) //cell is right edge and not top rigth or bottom right
        //{
        //    for (int i = m_col - 1; i < m_col; i++)
        //    {
        //        for (int j = m_row + 1; j < m_row - 1; j--)
        //        {
        //            if (!grid[i][j].m_isDead)
        //            {
        //                aliveNeighbors++;
        //            }
        //        }
        //    }
        //}
        //else if (m_row == gridSize && (m_col != 0 || m_col != gridSize)) // cell is top edge and not top right or top left
        //{
        //    for (int i = m_col - 1; i < m_col + 1; i++)
        //    {
        //        for (int j = m_row; j < m_row + 1; j--)
        //        {
        //            if (!grid[i][j].m_isDead)
        //            {
        //                aliveNeighbors++;
        //            }
        //        }
        //    }
        //}
        //else if (m_row == 0 && (m_col != 0 || m_col != gridSize))//cell is bottom edge and not bottom right or bottom left
        //{
        //    for (int i = m_col - 1; i < m_col + 1; i++)
        //    {
        //        for (int j = m_row + 1; j < m_row; j--)
        //        {
        //            if (!grid[i][j].m_isDead)
        //            {
        //                aliveNeighbors++;
        //            }
        //        }
        //    }
        //}
        //else if (m_col == 0 && m_row == gridSize) //cell is top left
        //{
        //    if (!grid[m_col - 1][m_row].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col + 1][m_row - 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col][m_row - 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //}
        //else if (m_col == gridSize && m_row == gridSize)//cell is top right
        //{
        //    if (!grid[m_col - 1][m_row].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col - 1][m_row - 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col][m_row - 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //}
        //else if (m_col == 0 && m_row == gridSize)//cell is bottom left
        //{
        //    if (!grid[m_col][m_row + 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col + 1][m_row + 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col][m_row + 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //}
        //else if (m_col == gridSize && m_row == 0)//cell is bottom right
        //{
        //    if (!grid[m_col - 1][m_row].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col - 1][m_row + 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //    if (!grid[m_col][m_row + 1].m_isDead)
        //    {
        //        aliveNeighbors++;
        //    }
        //}
        return aliveNeighbors;
    }

    //updates the cell based on the number of alive neighbors
    void updateHealth(int aliveNeighbors, Square** grid)
    {
        
        /*if (aliveNeighbors > 0)
        {
         if ((aliveNeighbors == 2 || aliveNeighbors == 3))
            {
                m_isDead = false;
            }
            else if (aliveNeighbors == 3)
            {
                m_isDead = false;
            }
            else
            {
               m_isDead = true;
            }
        }*/
        if ( aliveNeighbors < 2 && !m_isDead)
        {
            m_isDead = true;
        }
        else if ( aliveNeighbors > 3 && !m_isDead)
        {
            m_isDead = true;
        }
        else if (aliveNeighbors == 3 && m_isDead)
        {
            m_isDead = false;
        }
        else
        {
            m_isDead = grid[m_col][m_row].m_isDead;
        }

    }

private:
    //members
    float m_size = .05f;
    int m_col = 0; //relative to the grid set when creating grid
    int m_row = 0; //relative to the grid set when creating grid
    bool  m_isDead = true;
    

};

void drawGrid(int gridSize, Square** grid)
{
    //* Render here */
    glClear(GL_COLOR_BUFFER_BIT); // clear the screen

    for (int i = 0; i < gridSize; i++)
    {
        for (int j = 0; j < gridSize; j++)
        {
            grid[i][j].drawSquare(i, j);
        }
    }

    glFlush();
}

Square** createGrid(int gridSize)
{
    //create the grid of cells
    //array of squares
    Square** grid = new Square * [gridSize];
    for (int i = 0; i < gridSize; i++)
    {
        grid[i] = new Square[gridSize];
    }


    //output the cells x and y positions
    //initialize each cells location based on the grid
    for (int row = gridSize - 1; row >= 0; row--)
    {
        for (int col = 0; col < gridSize; col++)
        {
            grid[col][row].setCol(col);
            grid[col][row].setRow(row);
        }
    }

    return grid;
}

void printGridConsole(Square** grid, int gridSize)
{
    //PRINT GRID TEST
    for (int i = gridSize - 1; i >= 0; i--)
    {
        for (int j = 0; j < gridSize; j++)
        {
            cout << '[' << "Col-" << grid[i][j].getCol() << ':' << "Row-" << grid[i][j].getRow() << ']';
        }
        cout << '\n';
    }
}
//Square** evolve(Square** grid, int gridSize)
void evolve(Square ** grid, int gridSize)
{
    //Square** nextGrid = createGrid(gridSize);

    for(int i = 0; i < gridSize; i++)
    {
        for (int j = gridSize - 1; j >= 0; j--)
        {
            grid[i][j].updateHealth(grid[i][j].checkNeighbors(grid, gridSize), grid);
        }
    }

    //return grid;
}

Square** doEverything(Square** grid, int gridSize)
{
    Square** nextGrid = createGrid(gridSize);
    
    //copy the grid into a new grid
    for (int i = 0; i < gridSize; i++)
    {
        for (int j = 0; j < gridSize; j++)
        {
            nextGrid[i][j] = grid[i][j];
        }
    }

    //loop throught every cell
    for (int l = 1; l < gridSize - 1; l++)
    {
        for (int m = 1; m < gridSize - 1; m++)
        {
            //finding number of alive neighbors
            int aliveNeighbors = 0;
            for (int i = -1; i <= 1; i++)
            {
                for (int j = -1; j <= 1; j++)
                {
                    if (!grid[l + i][m + j].getIsDead())
                    {
                        aliveNeighbors++;
                    }
                }
            }
            //The cell needs to be subtracted from its neighbors as it was counted before
            if (!grid[l][m].getIsDead())
            {
                aliveNeighbors--;
            }

            //Implementing the Rules of Life

            //Cell is lonely and dies
            if (!grid[l][m].getIsDead() && (aliveNeighbors < 2))
                nextGrid[l][m].setIsDead(true);
            else if (!grid[l][m].getIsDead() && (aliveNeighbors > 3)) //Cell dies die to over population
            {
                nextGrid[l][m].setIsDead(true);
            }
            else if (grid[l][m].getIsDead() && (aliveNeighbors == 3)) // A new cell is born
            {
                nextGrid[l][m].setIsDead(false);
            }
            else //remains the same
            {
                nextGrid[l][m].setIsDead(grid[l][m].getIsDead());
            }
        }
    }

    return nextGrid;
}


//We are going to have a grid that gets passed the coordinates of the cell, each cell will remember its coordinates

int main(void)
{
    GLFWwindow* window;

    //values needed for the grid
    int gridSize = 40;

    Square** grid = createGrid(gridSize);

    

    // TODO: initialize the random alive or dead cells (this will later be done with mouse clicks and a start run function)
    //remember grid[0][0] is the bottom left

    // ------------- Spaceships ---------------------------
    //glider WORKS
    grid[3][25].setIsDead(false);
    grid[4][25].setIsDead(false);
    grid[4][26].setIsDead(false);
    grid[5][26].setIsDead(false);
    grid[3][27].setIsDead(false);

    //--------------- Oscillators --------------------------

    //Blinker WORKS
    /*grid[3][25].setIsDead(false);
    grid[4][25].setIsDead(false);
    grid[5][25].setIsDead(false);*/

    //Toad WORKS
    /*grid[3][25].setIsDead(false);
    grid[3][26].setIsDead(false);
    grid[3][27].setIsDead(false);
    grid[4][26].setIsDead(false);
    grid[4][27].setIsDead(false);
    grid[4][28].setIsDead(false);*/

    //Beacon WORKS
    /*grid[10][10].setIsDead(false);
    grid[11][10].setIsDead(false);
    grid[11][11].setIsDead(false);
    grid[10][11].setIsDead(false);

    grid[12][12].setIsDead(false);
    grid[13][12].setIsDead(false);
    grid[13][13].setIsDead(false);
    grid[12][13].setIsDead(false);*/

    //------------------ Still Lifes -----------------------

    //loaf WORK
    /*grid[10][10].setIsDead(false);
    grid[11][10].setIsDead(false);
    grid[12][9].setIsDead(false);
    grid[12][8].setIsDead(false);
    grid[9][9].setIsDead(false);
    grid[10][8].setIsDead(false);
    grid[11][7].setIsDead(false);*/

    //tub WORK
    /*grid[10][10].setIsDead(false);
    grid[9][9].setIsDead(false);
    grid[11][9].setIsDead(false);
    grid[10][8].setIsDead(false);*/


    /* Initialize the library */
    if (!glfwInit())
        return -1;

    /* Create a windowed mode window and its OpenGL context */
    window = glfwCreateWindow(600, 600, "Dan's Game of life", NULL, NULL); //640, 480
    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    /* Make the window's context current */
    glfwMakeContextCurrent(window);

    /* Loop until the user closes the window */
    while (!glfwWindowShouldClose(window))
    {
        drawGrid(gridSize, grid);
        this_thread::sleep_for(chrono::seconds(1));

        //check the neighbors of all the grids cells and update the nextGrids cells corispondingly
        //grid = evolve(grid, gridSize);
        //evolve(grid, gridSize);
        grid = doEverything(grid, gridSize);

        /* Swap front and back buffers */
        glfwSwapBuffers(window);

        /* Poll for and process events */
        glfwPollEvents();
    }

    //delete grid...? free grid
    for (int i = 0; i < gridSize; i++)
    {
        delete[] grid[i];
    }
    delete[] grid;

    glfwTerminate();
    return 0;
}




