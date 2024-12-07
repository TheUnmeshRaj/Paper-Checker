# **Automated OMR and QR Code Evaluation System**

## **Overview**
This project aims to automate the process of evaluating OMR sheets and QR codes to improve accuracy and efficiency. By integrating tools like OpenCV for OMR scanning and Python modules like ZBar for QR code processing, the system eliminates common issues such as illegible handwriting and manual data entry errors.

---

## **Features**
1. **QR Code Integration**  
   - Students fill out a form and receive a QR code with their details.  
   - The QR code acts as a hall ticket and is attached to the OMR sheet.  
   - Backup option: Names can still be written manually on the OMR sheet.

2. **Automatic OMR Evaluation**  
   - Scans and evaluates OMR sheets to retrieve marks.  
   - Marks can be processed part-wise or question-wise, as required.  
   - Results are stored in a table for easy export to Google Sheets or Forms.

3. **Manual Coding Question Evaluation**  
   - Part C, containing coding questions, is manually checked for logical and functional accuracy.

---

## **Why This System?**
- **Improves Data Accuracy**:  
   Handwriting issues can cause errors in critical fields like phone numbers and email IDs. This system ensures accurate data capture through QR codes.
  
- **Time-Saving**:  
   Automates tedious tasks like OMR sheet scanning and mark calculation.  
   
- **Customizable Outputs**:  
   Allows exporting results to Google Sheets or directly integrating them with Google Forms.

---

## **How It Works**
### **Step 1: Generate QR Codes**
1. Students fill an online form.  
2. A QR code is generated with their details (e.g., name, phone number, email ID, etc.).  
3. QR codes are printed and stapled to the respective OMR sheets.

### **Step 2: Scan and Evaluate**
1. **QR Code Scanning**:  
   - Use the ZBar Python module to scan QR codes and fetch student details automatically.  

2. **OMR Scanning**:  
   - Use OpenCV to process OMR sheets.  
   - Identify filled bubbles and calculate marks either part-wise or question-wise.  

3. **Store Results**:  
   - Results are saved in a structured format, ready for export to Google Sheets or Forms.

### **Step 3: Manual Evaluation (Part C)**  
Coding questions in Part C are evaluated manually due to their complexity.

---

## **Tools and Technologies**
- **Python Libraries**:  
   - OpenCV: For OMR sheet processing.  
   - ZBar: For QR code scanning and decoding.  

- **Optional Integrations**:  
   - Google Sheets API: For directly exporting results.  
   - Google Forms API: For automated data submission.

---

## **Future Enhancements**
1. Fully automate the data export to Google Forms or Sheets.  
2. Add AI-based evaluation for coding questions to reduce manual effort.  
3. Include a validation step to catch potential errors in OMR or QR code scanning.  

---

## **Setup Instructions**
1. Clone this repository:  
   ```bash
   git clone https://github.com/TheUnmeshRaj/Paper-Checker.git
   ```

2. Install dependencies:  
   ```bash
   pip install opencv-python zbar pillow google-api-python-client
   ```

3. Run the script:  
   ```bash
   python omr.py
   ```

---

## **Contributors**
- [Unmesh Raj](https://github.com/theunmeshraj)
