import gradio as gr
from datetime import datetime
from importlib import resources

def MindfulWebUI(client, address: str = None, port: int = None, browser: bool = True,
                 upload_size: str = "4MB", public: bool = False, limit: int = 1):
    """
    Start Mindful WebUI with all features.
    
    Parameters:
    - client (Client): Atelier Client instance
    - address (str): Server address
    - port (int): Server port
    - browser (bool): Launch browser automatically
    - upload_size (str): Maximum file size for uploads
    - public (bool): Enable public URL mode
    """
    try:
        version = client.version
        
        system_theme = gr.themes.Default(
            primary_hue=gr.themes.colors.rose,
            secondary_hue=gr.themes.colors.rose,
            neutral_hue=gr.themes.colors.zinc
        )
        
        css = str(resources.files(__name__) / "__4.38.1__.py")
        
        def Markdown(name:str):
            return gr.Markdown(f"{name}")

        def Textbox(name:str, lines:int=1, max_lines:int=4):
            return gr.Textbox(placeholder=f"{name}", lines=lines, max_lines=max_lines, container=False)

        def Button(name:str, variant:str='secondary'):
            return gr.Button(name, variant=variant, min_width=96)

        def Gallery(height:int):
            return gr.Gallery(height=height, object_fit="contain", container=False, show_share_button=False)

        def State(name:list):
            return gr.State(name)

        def truncate_prompt(prompt, max_length=50):
            if prompt is None or prompt == "": return "No Prompt"
            return (prompt[:max_length] + '...') if len(prompt) > max_length else prompt
        
        with gr.Blocks(title=f"Mindful Client {version}", css=css, analytics_enabled=False, theme=system_theme, fill_height=True).queue(default_concurrency_limit=limit) as demo:
            
            with gr.Row():
                with gr.Column(scale=1):
                    Markdown(f"## <br><center>Mindful Client {version}")
                    Markdown(f"<center>Copyright (C) 2023-{datetime.now().year} Ikmal Said. All rights reserved")
            
            with gr.Tab("Mindful Chat"):
                
                def preprocess(pro, ram):
                    caption = f"{truncate_prompt(pro)}"
                    results = client.generate_image(pro)
                    if results is not None:
                        for img in reversed(results):
                            ram.insert(0, (img, caption))
                    return ram
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=1) as menu:
                        Markdown(f"## <center>D3 Image Generator")
                        Markdown("<center>Basic Settings")
                        pro = Textbox("Prompt for image...", 5, 5)
                        sub = Button("Generate", "stop")
                    
                    with gr.Column(variant="panel", scale=3) as result:
                        res = Gallery(825)
                        ram = State([])
                        sub.click(
                            concurrency_limit=1,
                            show_progress='minimal',
                            show_api=False,
                            scroll_to_output=True,
                            fn=preprocess,
                            inputs=[pro, ram],
                            outputs=[res]
                        )

            Markdown("<center>Atelier D3 can make mistakes. Check important info. Request errors will return None.")

        demo.launch(
            server_name=address,
            server_port=port,
            inbrowser=browser,
            max_file_size=upload_size,
            share=public,
            quiet=True
        )
        
    except Exception as e:
        client.logger.error(f"Startup error: {e}")
        raise RuntimeError(f"Startup error: {e}")