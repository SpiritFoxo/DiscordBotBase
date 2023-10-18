#include <iostream>
#include <vector>
#include <time.h>

using namespace std;


int main()
{
    int count, s = 0;
    char ch;
    cout << "Size of numbers" << endl;
    cin >> count;
    cout << "Substract or add" << endl;
    cin >> ch;

    int* num1 = new int[count];
    int* num2 = new int[count];
    vector<int> result;
    for (int i = 0; i < count - 1; i++) {
        num1[i] = rand() % 10;
        num2[i] = rand() % 10;
    }
    int hnum1 = 0, hnum2 = 0;
    while (true) {
        hnum1 = rand() % 10;
        hnum2 = rand() % 10;
        if (hnum1 != 0 && hnum2 != 0) {
            break;
        }
    }
    num1[count - 1] = hnum1;
    num2[count - 1] = hnum2;

    for (int i = count - 1; i > 0; i--) {
        if (num1[i] > num2[i]){
            s = 1;
            break;
        }
        if (num1[i] < num2[i]) {
            s = 0;
            break;
        }
        if (i == 0) {
            s = 2;
            break;
        }
    }

    if (ch == '+'){

        for (int i = 0; i < count; i++) {
            if (i == 0) {
                result.push_back((num1[i] + num2[i]) % 10);
            }
            else if (i == count - 1) {
                result.push_back(((num1[i] + num2[i]) + (num1[i - 1] + num2[i - 1]) / 10));
            }
            else {
                result.push_back(((num1[i] + num2[i]) % 10 + (num1[i-1] + num2[i-1]) / 10) % 10);
            }
        }
    }

    if (ch == '-')
    {
        if (s == 2) {
            result.push_back(0);
        }

        if(s == 1){
            for (int i = 0; i < count; i++) {
                if (num1[i] >= num2[i]) {
                    result.push_back(num1[i] - num2[i]);
                }
                else
                {
                    num1[i + 1] = num1[i + 1] - 1;
                    result.push_back(num1[i] + 10 - num2[i]);
                }

            }
        }

        if (s == 0) {
            for (int i = 0; i < count; i++) {
                if (num2[i] >= num1[i]) {
                    result.push_back(num2[i] - num1[i]);
                }

                else
                {
                    num2[i+1] = num2[i + 1] - 1;
                    result.push_back(num2[i] + 10 - num1[i]);
                }

            }

        }
    }

    for (int i = count - 1; i >= 0; i--) {
        cout << num1[i];
    }
    cout << endl;
    for (int i = count - 1; i >= 0; i--) {
        cout << num2[i];
    }
    reverse(result.begin(), result.end());
    cout << endl;
    for (int i = 0; i < result.size(); i++) {
        if (i == 0 && result[i] == 0) {
            cout << "";
        }
        else
        {
            cout << result.at(i);
        }
    }
}
