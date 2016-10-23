using System;
using System.Text;
using System.Windows;
using System.Net.Sockets;
using Microsoft.VisualBasic;

namespace SPRO3CustomerInterface
{
	public partial class MainWindow: Window
	{
		public MainWindow()
		{
			InitializeComponent();
		}

		private void button_Click(object sender, RoutedEventArgs e)
		{
			/* Server IP and port for Kitchen */
			string TCP_IP_KIT = "10.0.1.15";
			Int32 TCP_PORT_KIT = 5005;

			/* Interaction boxes to get order information and room number from
			 * user */																				
			string order = Interaction.InputBox("Please be clear with your " + 
				"order, and follow the menu.\nIf we have trouble " + 
				"understanding, we will contact you.", "Room Service",
				"Enter your order");
			if(order == "")
				return;

			string roomnr = Interaction.InputBox("What is your room number?",
				"Room Service", "Enter your room number");
			if(roomnr == "")
				return;

			/* Sends order and room number to Kitchen */
			Tcp.Send(TCP_IP_KIT, TCP_PORT_KIT, order);
			bool check = Tcp.Send(TCP_IP_KIT, TCP_PORT_KIT, roomnr);

			/* Checks the value returned from Tcp.Send and informs the user 
			 * Value 'false' can be given as a result of unsuccessful 
			 * communication between the user and the Kitchen, or the Kitchen 
			 * and the Raspberry Pi */
			if(check) {
				MessageBox.Show("On our way!", "Order received");
			} else {
				MessageBox.Show("Your order has not been processed. Please " +
					"try again later.", "Server Communication Failure");
			}
		}
	}

	public class Tcp
	{
		public static bool Send(String server, Int32 port, String msg)
		{
			try {
				TcpClient client = new TcpClient(server, port);

				/* Stores message to be sent as a Byte array (ASCII) */
				Byte[] data = Encoding.ASCII.GetBytes(msg);

				/* Get client stream for reading and writing */
				NetworkStream stream = client.GetStream();

				/* Sends data to server */
				stream.Write(data, 0, data.Length);

				/* Buffer to store response bytes */
				data = new Byte[256];

				String responseData = String.Empty;

				/* Gets data back from server (if communication was successful
				 * or not */
				Int32 bytes = stream.Read(data, 0, data.Length);
				responseData = Encoding.ASCII.GetString(data, 0, bytes);

				/* Closes stream and client */
				stream.Close();
				client.Close();

				/* If communication to Kitchen was successful, value sent by
				 * Kitchen is returned */
				return Convert.ToBoolean(responseData);

			} catch(ArgumentNullException e){
				/* If communicaton unsuccessful, value 'false' is returned */
				return false;
			} catch(SocketException e) {
				/* If communication unsuccessful, value 'false' is returned */
				return false;
			}
		}
	}
}
