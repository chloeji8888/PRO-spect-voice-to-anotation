import streamlit as st
import json
from utils.transcriber import RealTimeTranscriber, TextInference  # Ensure this import matches the correct module path

# def extract_candidate_info(text):
#     # Initialize TextInference for analyzing text
#     text_inference = TextInference()

#     # Create a prompt for the AI to extract information
#     prompt = f"""
#     Extract the following information from the given text and format it as JSON:
#     - Name
#     - School
#     - Degree
#     - Graduation Year
#     - Work Experience (list of companies and positions)
#     - Skills

#     Text: {text}

#     JSON format:
#     """

#     # Generate the JSON response
#     response = text_inference.process_text(prompt)

#     # Parse the JSON response
#     try:
#         candidate_info = json.loads(response)
#         print(candidate_info)
#     except json.JSONDecodeError:
#         st.error("Failed to parse the extracted information. Please try again.")
#         return None

#     return candidate_info

# def main():
#     st.title("Nexa AI Voice Transcription")
#     st.caption("Powered by Nexa AI SDK🐙")

#     st.sidebar.header("Model Configuration")

#     # Sidebar inputs for model configuration
#     model_path = st.sidebar.text_input("Model Path", "faster-whisper-tiny")
#     beam_size = st.sidebar.slider("Beam Size", 1, 10, 5)
#     task = st.sidebar.selectbox("Task", ["transcribe", "translate"], index=0)
#     temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.0, step=0.1)
#     language = st.sidebar.text_input("Language", "").strip()

#     # Use None if the language input is empty
#     language = language if language else None

#     transcriber = RealTimeTranscriber(
#         model_path=model_path,
#         beam_size=beam_size,
#         task=task,
#         temperature=temperature,
#         language=language
#     )

#     # Initialize TextInference for generating summaries
#     text_inference = TextInference()

#     # Initialize transcription in session state if not already initialized
#     if "transcription" not in st.session_state:
#         st.session_state["transcription"] = ""

#     # Placeholder for transcription outside the columns for full width
#     transcription_container = st.empty()
#     transcription_container.text_area("Transcription", value=st.session_state["transcription"], height=300, key="transcription_area")

#     # Start and Stop buttons
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         if st.button("Start Recording"):
#             transcriber.start_recording_foreground(transcription_container)

#     with col2:
#         if st.button("Stop"):
#             transcriber.stop_recording_foreground(transcription_container)

#     with col3:
#         if st.button("Reset"):
#             transcriber.reset_transcription()

#     with col4:
#         # Display download button directly without requiring another click
#         if st.session_state["transcription"]:
#             transcription_bytes = st.session_state["transcription"].encode()
#             st.download_button(
#                 label="Download Transcription",
#                 data=transcription_bytes,
#                 file_name="transcription.txt",
#                 mime="text/plain",
#             )

#     # File uploader for transcription
#     uploaded_file = st.file_uploader("Upload a .wav file", type=["wav"])
#     if uploaded_file is not None:
#         if st.button("Transcribe Uploaded Audio"):
#             with st.spinner("Transcribing uploaded audio..."):
#                 transcription = transcriber.transcribe_audio(uploaded_file)
#             if transcription:
#                 st.session_state["transcription"] += transcription
#                 transcription_container.text_area("Transcription", value=st.session_state["transcription"], height=300, key="transcription_area_uploaded")
#             else:
#                 st.error("Transcription failed. Please try again.")

#     # Button to generate summary
#     if st.session_state["transcription"] and st.button("Generate Summary"):
#         with st.spinner("Generating summary..."):
#             summary_prompt = f"Please summarize the following transcription:\n\n{st.session_state['transcription']}\n\nSummary:"
#             summary = ""
#             summary_area = st.empty()

#             for i, chunk in enumerate(text_inference.generate_summary(summary_prompt)):
#                 if not chunk:
#                     continue
                
#                 summary += chunk
#                 summary_area.text_area("Summary", value=summary, height=200)

#             st.session_state["summary"] = summary

#     # Status message
#     st.write(st.session_state.get("recording_status", "Press 'Start Recording' to begin."))

def main():
    st.title("Candidate Analysis Tool")
    st.caption("Powered by Nexa AI SDK🐙")

    # Text area for transcript input
    transcript = st.text_area("Enter the candidate's transcript here:", height=300)
    

    if st.button("Analyze Transcript"):
        if transcript:
            with st.spinner("Analyzing transcript..."):
                text_inference = TextInference()
                candidate_info = text_inference.extract_candidate_info(transcript)
                if candidate_info:
                    st.subheader("Extracted Candidate Information")
                    st.json(candidate_info)
                else:
                    st.error("Failed to extract candidate information. Please try again.")
        else:
            st.warning("Please enter a transcript to analyze.")

    # File uploader for transcript files
    uploaded_file = st.file_uploader("Or upload a transcript file", type=["txt"])
    if uploaded_file is not None:
        if st.button("Analyze Uploaded Transcript"):
            with st.spinner("Analyzing uploaded transcript..."):
                transcript = uploaded_file.getvalue().decode("utf-8")
                candidate_info = extract_candidate_info(transcript)
                if candidate_info:
                    st.subheader("Extracted Candidate Information")
                    st.json(candidate_info)

                    # Option to download the JSON
                    json_string = json.dumps(candidate_info, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_string,
                        file_name="candidate_info.json",
                        mime="application/json"
                    )

if __name__ == "__main__":
    main()