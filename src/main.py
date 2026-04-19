import os
import sys
from dotenv import load_dotenv

# Add src to Python Path so script can be executed nicely
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from document_processor import setup_retriever
from agent import AgenticRAG

def main():
    # Load environment variables (api keys)
    load_dotenv()
    
    print("=== Agentic RAG System ===")
    print("Setting up document index. Please wait...")
    
    # Phase 1 setup
    try:
        # Assumes this script is run from the project root
        data_dir = os.path.join(os.getcwd(), "data")
        db_dir = os.path.join(os.getcwd(), "chroma_db")
        retriever = setup_retriever(data_dir=data_dir, persist_directory=db_dir)
        agent = AgenticRAG(retriever=retriever)
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        return
    except Exception as e:
        print(f"\nInitialization Error: {e}")
        return
        
    print("\nSystem ready! Type 'exit' or 'quit' to stop.")
    print("---------------------------------------------")
    
    # Interactive loop for user interaction
    while True:
        try:
            print()
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            print(f"Thinking...", flush=True)
            result = agent.ask(user_input)
            
            print("\n" + "="*60)
            print("Answer:")
            print(result["answer"].strip())
            print("\n- - - - - - - - - - - - - - - - - - - - - - - -")
            
            # Map reasoning_type to specific labels
            label_map = {
                "RAG": "Yes, context searched",
                "MEMORY": "No, used memory",
                "GENERAL": "No, general knowledge used"
            }
            label = label_map.get(result["reasoning_type"], "General Knowledge Used")
            print(f"Retrieval Used: {label}")
            
            if result["reasoning_type"] == "RAG" and result["sources"]:
                print("Sources:")
                for source in result["sources"]:
                    print(f"  - {source}")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
