- Location should be selected via a dropdown instead of manual input.
- Add an optional "Extra Preferences" field where users can type custom preferences (e.g., family-friendly, outdoor seating). Update the prompt logic to include this field when provided.
- Cuisine should be optional and not mandatory for the user to fill.

New Improvements:
1. Text alignment issue
The description text (“Let Zomato AI find…”) is appearing vertically instead of properly aligned in a single horizontal paragraph.

2. Location dropdown missing
The location field no longer shows dropdown/autocomplete suggestions.
Previously implemented dropdown/select feature is removed.

3. Budget input incorrect
Budget is currently shown as a slider/scale.
Requirement: It should be a simple input field where users can manually enter the amount.

4. Unwanted text inside input fields
Text like:
location_on
restaurant
payments
psychology
These should be removed from input boxes.

5. Button text issue
Button currently shows: “search Find Places”
Requirement: Only “Find Places” should be displayed.

6. Incorrect currency symbol
Indian currency symbol (₹) is showing in results.
Requirement: Show correct currency symbol based on user's location

7. Dummy data instead of real data
Currently showing placeholder/dummy restaurants.
Requirement:
Show real restaurants from dataset
Display actual:
Restaurant name
Location
Price (₹)
Also include cuisine/type of food offered, such as:
Italian
Chinese
North Indian
etc.
Each restaurant card should clearly show what kind of food the restaurant offers