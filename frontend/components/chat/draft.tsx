// notes- ne

// import { useState, useRef, useEffect } from "react";
// import { ChatHeader } from "@/components/ChatHeader";
// import { GuidelinesPanel } from "@/components/GuidelinesPanel";
// import { DraggableDivider } from "@/components/DraggableDivider";
// import { WelcomePanel } from "@/components/WelcomePanel";

// interface Message {
//   id: string;
//   type: "user" | "assistant";
//   content: string;
// }

// const defaultMessages: Message[] = [
//   {
//     id: "1",
//     type: "assistant",
//     content:
//       "Hi, thanks for uploading the dataset to ADaS. Ask me about:\n• Time range\n• Top n anomalies (n is the number of anomalies)\n• Number of features used to identify anomalies.\n  - For example, 6, 8, 10 features. We recommend you to start with 10 features for optimal result. Note, ADaS will run the experiment if you ask it to run with a different number of features. For example, asking 12 features running with 10 features.\n• Explanation\n  You can ask to provide context associated with IP address x",
//   },
//   {
//     id: "2",
//     type: "assistant",
//     content:
//       'You should not query like these bad examples:\n• "Tell me what are the anomalies under feature timestamp"\n  Instead, specify the number of features.\n• "I want to know the output with 10, 1s, and 5s features."\n  Instead, try query with features first, save the result. Query with 12 features.',
//   },
//   {
//     id: "3",
//     type: "assistant",
//     content: "Now, let's try it yourself. You can start typing on the right.",
//   },
// ];

// export default function Index() {
//   const [messages, setMessages] = useState<Message[]>(defaultMessages);
//   const [inputValue, setInputValue] = useState("");
//   const [leftPanelWidth, setLeftPanelWidth] = useState(50);
//   const containerRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     const handleMouseMove = (e: MouseEvent) => {
//       if (!containerRef.current) return;

//       const container = containerRef.current;
//       const rect = container.getBoundingClientRect();
//       const newWidth = ((e.clientX - rect.left) / rect.width) * 100;

//       if (newWidth > 20 && newWidth < 80) {
//         setLeftPanelWidth(newWidth);
//       }
//     };

//     const handleMouseUp = () => {
//       document.removeEventListener("mousemove", handleMouseMove);
//       document.removeEventListener("mouseup", handleMouseUp);
//     };

//     const handleDividerMouseDown = () => {
//       document.addEventListener("mousemove", handleMouseMove);
//       document.addEventListener("mouseup", handleMouseUp);
//     };

//     const divider = containerRef.current?.querySelector('[data-divider]');
//     if (divider) {
//       divider.addEventListener("mousedown", handleDividerMouseDown);
//     }

//     return () => {
//       if (divider) {
//         divider.removeEventListener("mousedown", handleDividerMouseDown);
//       }
//     };
//   }, []);

//   const handleSendMessage = (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!inputValue.trim()) return;

//     const userMessage: Message = {
//       id: Date.now().toString(),
//       type: "user",
//       content: inputValue,
//     };

//     const assistantMessage: Message = {
//       id: (Date.now() + 1).toString(),
//       type: "assistant",
//       content:
//         "I understand your query. I'm analyzing your dataset for anomalies based on your specifications.",
//     };

//     setMessages([...messages, userMessage, assistantMessage]);
//     setInputValue("");
//   };

//   const handleNewChat = () => {
//     setMessages(defaultMessages);
//     setInputValue("");
//   };

//   return (
//     <div className="flex h-screen bg-white overflow-hidden flex-col">
//       <ChatHeader onNewChat={handleNewChat} />

//       {/* Main Content Area */}
//       <div ref={containerRef} className="flex-1 flex overflow-hidden relative">
//         <GuidelinesPanel messages={messages} panelWidth={leftPanelWidth} />
//         <DraggableDivider />
//         <WelcomePanel
//           panelWidth={100 - leftPanelWidth}
//           onQuerySelect={setInputValue}
//           inputValue={inputValue}
//           onInputChange={setInputValue}
//           onInputSubmit={handleSendMessage}
//         />
//       </div>
//     </div>
//   );
// }





// Here are the specific code sections you asked about:

// 1. Dragging Effect Code (Lines 40-72)
// useEffect(() => {
//   const handleMouseMove = (e: MouseEvent) => {
//     if (!containerRef.current) return;

//     const container = containerRef.current;
//     const rect = container.getBoundingClientRect();
//     const newWidth = ((e.clientX - rect.left) / rect.width) * 100;

//     if (newWidth > 20 && newWidth < 80) {
//       setLeftPanelWidth(newWidth);
//     }
//   };

//   const handleMouseUp = () => {
//     document.removeEventListener("mousemove", handleMouseMove);
//     document.removeEventListener("mouseup", handleMouseUp);
//   };

//   const handleDividerMouseDown = () => {
//     document.addEventListener("mousemove", handleMouseMove);
//     document.addEventListener("mouseup", handleMouseUp);
//   };

//   const divider = containerRef.current?.querySelector('[data-divider]');
//   if (divider) {
//     divider.addEventListener("mousedown", handleDividerMouseDown);
//   }

//   return () => {
//     if (divider) {
//       divider.removeEventListener("mousedown", handleDividerMouseDown);
//     }
//   };
// }, []);
// How it works:

// handleMouseMove - Calculates the new width percentage as mouse moves
// handleMouseUp - Stops dragging when mouse is released
// handleDividerMouseDown - Starts listening to mouse movement when divider is clicked
// Min/max constraints: 20% < width < 80% prevents panels from becoming too small
// 2. Panel Width Styling (Lines 134-147 & 197-203)
// Left Panel (with dynamic width):

// <div
//   style={{ width: `${leftPanelWidth}%` }}
//   className="border-r border-gray-200 bg-white flex flex-col overflow-hidden transition-none"
// >
// Right Panel (complementary width):

// <div
//   style={{ width: `${100 - leftPanelWidth}%` }}
//   className="bg-gray-50 flex flex-col overflow-hidden transition-none"
// >
// Draggable Divider (Line 189-195):

// <div
//   data-divider="true"
//   className="w-1 bg-gray-200 hover:bg-gray-400 cursor-col-resize transition-colors flex-shrink-0 select-none"
// />
// State variable (Line 35):

// const [leftPanelWidth, setLeftPanelWidth] = useState(50); // Starts at 50%
// 3. Query Box Click Handler (Lines 230-252)
// <div
//   onClick={() =>
//     setInputValue(
//       "Tell me the IP address of the top anomalies in the dataset."
//     )
//   }
//   className="p-4 bg-white rounded-lg hover:bg-gray-100 cursor-pointer transition-colors text-gray-600 text-sm leading-relaxed border border-gray-200"
// >
//   Tell me the IP address of the top anomalies in the dataset.
// </div>
// The key is onClick={() => setInputValue("your text here")}

// This sets the inputValue state, which is connected to the message input:

// <input
//   type="text"
//   value={inputValue}
//   onChange={(e) => setInputValue(e.target.value)}
//   placeholder="Message..."
// />
// So clicking any query box updates the input field with that text, and users can edit it or click send to submit.