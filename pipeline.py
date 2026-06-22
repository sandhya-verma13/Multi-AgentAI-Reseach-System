from agents import build_search_agent, build_reader_agent,writer_chain,critic_chain

def run_research_pipeline(topic: str)->dict:
    state = {}

    # search agent working 
    print("\n"+" ="*50)
    print("step 1: Search Agent is gathering information on the topic...       ")
    print(" ="*50)

    search_agent = build_search_agent()
    search_result=search_agent.invoke({
        "messages":[{
"role": "user",
"content": f"Find recent and reliable information on the topic: {topic}" }]   

    })
    state["search_result"]=search_result['messages'][-1].content
    print("\n search result",state["search_result"])

    # step 2: reader agent working
    print("\n"+" ="*50)
    print("step 2: Reader Agent is scraping the URLs found in the search results...       ")
    print(" ="*50)

    reader_agent = build_reader_agent()
    reader_result=reader_agent.invoke({
        
        "messages":[{
        "role": "user",
        "content": f"Based on the following search result about the '{topic}', Pick the most relevant URL and scrape it..."
    }]
        
      
    })
    state['scraped_content']=reader_result['messages'][-1].content

    print("\n scraped content",state['scraped_content'])


    # step 3: writer chain working
    print("\n"+" ="*50) 
    print("step 3: Writer Chain is generating the research report...       ")
    print(" ="*50)

    research_combined=(
        f"Search Result:\n{state['search_result']}\n\nScraped Content:\n{state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Research Report:\n",state['report'])

    # critic report working
    print("\n"+" ="*50)
    print("step 4: Critic Chain is evaluating the research report...       ")
    print(" ="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n Critic Feedback:\n",state['feedback'])

    return state

if __name__=="__main__":
    topic = input("\nEnter the research topic: ")
    run_research_pipeline(topic)


    
    

    






    
    
    
    
    

    