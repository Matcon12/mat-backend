export default function ConsigeeDetails({
  name,
  address,
  address2,
  state,
  city,
  code,
  pin,
  gst_no,
}) {
  return (
    <div>
      <h3>Details of Consignee(Shipped to)</h3>
      <table className="receiver-address">
        <tbody>
          <tr>
            <td className="receiver-name">
              <strong>Name</strong>
            </td>
            <td className="receiver-dots">&nbsp;:&nbsp;</td>
            <td>{name}</td>
          </tr>
          <tr>
            <td>
              <strong>Address</strong>
            </td>
            <td>&nbsp;:&nbsp;</td>
            <td className="table-address">
              <p>
                {address}
                {address2 && (
                  <>
                    <br />
                    {address2}
                  </>
                )}
                <br />
                {city}-{pin}
              </p>
            </td>
          </tr>
          <tr>
            <td>
              <strong>State</strong>
            </td>
            <td>&nbsp;:&nbsp;</td>
            <td>{state}</td>
          </tr>
          <tr>
            <td>
              <strong>State Code</strong>
            </td>
            <td>&nbsp;:&nbsp;</td>
            <td>{code}</td>
          </tr>
          <tr>
            <td>
              <strong>GST No</strong>
            </td>
            <td>&nbsp;:&nbsp;</td>
            <td>
              <b>{gst_no}</b>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
