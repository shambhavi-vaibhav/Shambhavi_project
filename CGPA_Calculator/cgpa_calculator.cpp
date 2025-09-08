#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

// Function to convert grade to grade points
double gradeToPoint(string grade) {
    if (grade == "O" || grade == "o") return 10.0; // Outstanding
    else if (grade == "A+" || grade == "a+") return 9.0;
    else if (grade == "A" || grade == "a") return 8.0;
    else if (grade == "B+" || grade == "b+") return 7.0;
    else if (grade == "B" || grade == "b") return 6.0;
    else if (grade == "C" || grade == "c") return 5.0;
    else if (grade == "F" || grade == "f") return 0.0; // Fail
    else {
        cout << "Invalid grade entered! Defaulting to 0.\n";
        return 0.0;
    }
}

int main() {
    int subjects;
    cout << "==============================\n";
    cout << "      CGPA CALCULATOR\n";
    cout << "==============================\n";

    cout << "Enter number of subjects: ";
    cin >> subjects;

    double totalCredits = 0.0, weightedSum = 0.0;

    for (int i = 1; i <= subjects; i++) {
        string grade;
        double credit;
        cout << "\nSubject " << i << ":\n";
        cout << "Enter grade (O, A+, A, B+, B, C, F): ";
        cin >> grade;
        cout << "Enter credit hours: ";
        cin >> credit;

        double gradePoint = gradeToPoint(grade);
        weightedSum += gradePoint * credit;
        totalCredits += credit;
    }

    if (totalCredits == 0) {
        cout << "\nError: Total credits cannot be zero.\n";
        return 1;
    }

    double cgpa = weightedSum / totalCredits;

    cout << "\n==============================\n";
    cout << fixed << setprecision(2);
    cout << "Your CGPA is: " << cgpa << endl;
    cout << "==============================\n";

    if (cgpa >= 9) cout << "Excellent Performance! 🎉\n";
    else if (cgpa >= 8) cout << "Very Good Performance!\n";
    else if (cgpa >= 7) cout << "Good, keep improving!\n";
    else if (cgpa >= 6) cout << "Satisfactory, but work harder!\n";
    else cout << "Needs improvement. Don't give up!\n";

    return 0;
}
