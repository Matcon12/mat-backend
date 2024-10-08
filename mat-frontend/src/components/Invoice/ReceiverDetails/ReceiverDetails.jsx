export default function ReceiverDetails({
  name,
  address,
  address2,
  state,
  city,
  code,
  pin,
  gst_no,
  gst_exception,
}) {
  return (
    <div>
      <h3>Details of Receiver(Billed to)</h3>
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
                <br />
                {address2}
                <br />
                {city} - {pin}
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
          {gst_exception && (
            <tr>
              <td>
                <strong>GST Exception</strong>
              </td>
              <td>&nbsp;:&nbsp;</td>
              <td>
                <b>{gst_exception}</b>
              </td>
            </tr>
          )}
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
