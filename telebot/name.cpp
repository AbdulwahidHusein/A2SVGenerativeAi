#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

int main()
{
    int x;
    cin >> x;

    for (int i = 0; i < x; i++)
    {
        int y;
        cin >> y;
        vector<int> num(y);
        for (int j = 0; j < y; j++)
        {
            cin >> num[j];
        }
        vector<int> stack;
        for (int j = y - 1; j >= 0; j--)
        {
            if (find(stack.begin(), stack.end(), num[j]) == stack.end())
            {
                stack.push_back(num[j]);
            }
            else
            {
                break;
            }
        }
        cout << num.size() - stack.size() << endl;
    }

    return 0;
}