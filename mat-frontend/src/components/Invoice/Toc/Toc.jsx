export default function Toc() {
  return (
    <div className="toc-signature-container">
      <b>Certified that the Particulars given above are true and correct</b>
      <table className="toc-table">
        <tbody>
          <tr>
            <td>
              <div className="toc-container">
                <b>TERMS AND CONDITIONS OF SALE</b>
                <p>AS PER PO TERMS</p>
                &nbsp;
                <b>Our Bankers (NEFT/RTGS details):</b>
                <p className="address-word-break">
                  SBI, NRI Hebbal Branch <br /> A/c N. 41318044557 <br /> IFSC
                  Code. SBIN0016858
                </p>
              </div>
            </td>
            <td>
              <p>FOR MATCON</p>
              &nbsp;
              <div className="white-space"></div>
              {/* <p>For Authorized Signatory</p> */}
              <p className="align-start">
                <b>Name: </b>Uma V Murthy
              </p>
              <p className="align-start">
                <b>Designation: </b>Manager Commercial
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
