import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

# Potentially import Manim components here later if generating script directly
# from manim import Scene, Text, ImageMobject, FadeIn, Create, ...

from leap.core.config import GENERATED_DIR
# We might need FileService to save the script, or other services
from .file_service import FileService


class RAGAnimationService:
    """
    Service for Retrieval Augmented Generation (RAG) to create Manim animations.
    It takes a prompt, searches for relevant information, processes it,
    and generates a Manim animation script, including scraped media.
    """

    def __init__(self, file_service: Optional[FileService] = None): # Add other services as needed
        self.logger = logging.getLogger("leap.rag_animation_service")
        self.file_service = file_service or FileService()
        
        self.manim_scripts_dir = GENERATED_DIR / "manim_scripts"
        self.manim_scripts_dir.mkdir(parents=True, exist_ok=True)
        
        self.manim_media_output_dir = GENERATED_DIR / "manim_media" # Renamed for clarity
        self.manim_media_output_dir.mkdir(parents=True, exist_ok=True)

        self.rag_assets_dir = GENERATED_DIR / "rag_assets" # For downloaded images/videos
        self.rag_assets_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("RAGAnimationService initialized.")
        self.logger.info(f"Manim scripts will be saved to: {self.manim_scripts_dir}")
        self.logger.info(f"Manim media output will be directed to: {self.manim_media_output_dir}")
        self.logger.info(f"Downloaded RAG assets will be stored in: {self.rag_assets_dir}")


    async def generate_animation_from_prompt(self, prompt: str) -> str:
        """
        Generates a Manim animation from a text prompt.

        Args:
            prompt: The user's prompt to generate an animation for.

        Returns:
            A message indicating the outcome or path to the generated script/media.
        """
        self.logger.info(f"Received prompt: {prompt}")

        # 1. Retrieve information using web search (RAG part)
        # This includes text and ideally, direct links to media.
        retrieved_data = await self._search_web_and_extract_media(prompt)

        if not retrieved_data or not retrieved_data.get("processed_text"):
            self.logger.warning("No meaningful data retrieved or processed for the prompt.")
            return "Could not find or process relevant information for the prompt."

        # 2. Download media (conceptual for now, will need implementation)
        # local_media_paths = await self._download_media(retrieved_data.get("image_urls", []))
        # For now, we'll pass mock local paths or just the URLs to the script generator
        
        # 3. Process content and create Manim script
        animation_script_content = self._process_content_and_create_manim_script(
            prompt,
            retrieved_data["processed_text"],
            retrieved_data.get("image_urls", []) # Pass image URLs
        )
        
        # 4. Save the Manim script
        script_filename_base = f"animation_script_{self._sanitize_prompt(prompt)}"
        
        # Use the FileService, but ensure it saves to the manim_scripts_dir
        # We might need to adjust FileService or how we call it if it has a fixed base_dir
        # For now, let's construct the path directly if FileService is for general code
        
        script_path = self.manim_scripts_dir / f"{script_filename_base}_{self.file_service.sanitize_filename(datetime.now().strftime('%Y%m%d_%H%M%S'))}.py"
        
        with open(script_path, "w") as f:
            f.write(animation_script_content)
        self.logger.info(f"Manim script saved to: {script_path}")

        # 4. (Optional) Render the animation
        # This would involve calling Manim CLI.
        # e.g., manim -ql {script_path} SceneName -o {self.media_output_dir}
        # media_path = self._render_manim_script(script_path)

        return f"Manim script generated and saved to: {script_path}. Based on retrieved data for: {prompt}."

    async def _search_web_and_extract_media(self, query: str) -> dict:
        """
        Placeholder: Simulates web search, basic text processing, and media URL extraction.
        In a real scenario, this would involve:
        1. Calling the web_search tool.
        2. For each URL in search results:
            a. Fetching the page content.
            b. Parsing HTML to extract main text and image/video URLs.
            c. Storing these (e.g., in self.rag_assets_dir after download).
        """
        self.logger.info(f"Simulating web search and media extraction for: {query}")

        # Using the actual prompt for more relevant simulated data
        if "saudi-us 600 billion dollar deal" in query.lower():
            # Based on previous actual search results
            processed_text = [
                {"type": "title", "content": "The Saudi-US $600 Billion Deal"},
                {"type": "point", "content": "A significant economic partnership involving substantial Saudi investment in the US and major US defense sales to Saudi Arabia."},
                {"type": "heading", "content": "Key Areas of Impact for the US Economy:"},
                {"type": "bullet", "content": "Saudi Investment in US: ~$600B. E.g., DataVolt ($20B in AI/energy), various tech firms ($80B)."},
                {"type": "bullet", "content": "Job Creation: Across tech, energy, defense, healthcare."},
                {"type": "image_placeholder", "text_before": "Visualizing US Tech Investment:", "image_url": "https://example.com/images/ai_investment.jpg", "caption": "AI and Tech Hubs"},
                {"type": "heading", "content": "US Exports & Services:"},
                {"type": "bullet", "content": "Infrastructure Projects: $2B in US service exports (e.g., King Salman Airport)."},
                {"type": "bullet", "content": "Manufacturing: GE (turbines, $14.2B), Boeing (aircraft, $4.8B)."},
                {"type": "image_placeholder", "text_before": "Boeing Aircraft Example:", "image_url": "https://example.com/images/boeing_plane.jpg", "caption": "Boeing 737-8"},
                {"type": "heading", "content": "Defense Sector Boost:"},
                {"type": "bullet", "content": "$142B in US defense sales to Saudi Arabia, supporting US defense industry."},
                {"type": "image_placeholder", "text_before": "Advanced Defense Systems:", "image_url": "https://example.com/images/defense_system.png", "caption": "US Defense Technology"},
                {"type": "summary", "content": "Overall, the deal aims to strengthen economic ties, boost US industries, and enhance national security cooperation."}
            ]
            image_urls = [
                "https://example.com/images/ai_investment.jpg",
                "https://example.com/images/boeing_plane.jpg",
                "https://example.com/images/defense_system.png"
            ]
            
            return {"processed_text": processed_text, "image_urls": image_urls}
        else:
            # Generic fallback
            return {
                "processed_text": [
                    {"type": "title", "content": query[:60]},
                    {"type": "point", "content": "No specific mock data for this query. This is a general structure."}
                ],
                "image_urls": ["https://example.com/images/generic_placeholder.jpg"]
            }

    async def _download_media(self, urls: list[str]) -> dict[str, Path]:
        """
        Placeholder: Downloads media from URLs to self.rag_assets_dir.
        Returns a dictionary mapping original URLs to local file Paths.
        This would involve HTTP requests, saving files, and error handling.
        """
        self.logger.info(f"Conceptual: Downloading media from {len(urls)} URLs.")
        local_paths = {}
        for url in urls:
            try:
                filename = Path(url).name
                if not filename: # if URL ends in / or has no clear filename
                    filename = f"{self._sanitize_prompt(Path(url).stem)}_{Path(url).suffix}" if Path(url).suffix else f"{self._sanitize_prompt(Path(url).stem)}.jpg"

                local_path = self.rag_assets_dir / filename
                # In reality:
                # response = await http_client.get(url)
                # response.raise_for_status()
                # with open(local_path, "wb") as f:
                #     f.write(response.content)
                # self.logger.info(f"Downloaded {url} to {local_path}")
                local_paths[url] = local_path # Store the conceptual path
            except Exception as e:
                self.logger.error(f"Failed to prepare download path for {url}: {e}")
        return local_paths


    def _process_content_and_create_manim_script(
        self, 
        prompt: str, 
        processed_data: list[dict], # Expects a list of dicts with "type" and "content"
        image_urls: list[str] # These are the original URLs
    ) -> str:
        """
        Processes structured data and generates a Manim Python script,
        incorporating text and placeholders/instructions for images.
        """
        self.logger.info("Processing content and generating Manim script with media focus...")

        # Manim scene construction logic
        script_parts = [
            "from manim import *",
            "import os", # For joining paths
            "",
            f"# Manim script generated for prompt: {prompt}",
            f"# Assumes images are downloaded to: {self.rag_assets_dir}",
            "",
            "class GeneratedExplainerScene(Scene):",
            "    def construct(self):",
            f"        assets_dir = r'{str(self.rag_assets_dir).replace('\\\\', '/')}'", # Raw string for Windows paths
            "",
            "        current_y_pos = 3.5  # Start from top",
            "        elements_to_fade_out = VGroup()", # Use VGroup for easier fade out
            ""
        ]

        # Simulate mapping URLs to local downloaded paths (as _download_media would do)
        # For script generation, we use the URL's filename as a placeholder.
        mock_local_image_paths = {
            url: self.rag_assets_dir / Path(url).name for url in image_urls # just the filename part
        }
        
        for item_index, item in enumerate(processed_data):
            item_type = item.get("type")
            content = item.get("content", "")
            content_clean = content.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\\\n') # Clean for Manim Text

            if item_type == "title":
                script_parts.append(f"        title = Tex(r\"{content_clean}\", font_size=36).to_edge(UP)")
                script_parts.append("        self.play(Write(title))")
                script_parts.append("        elements_to_fade_out.add(title)")
                script_parts.append("        self.wait(1)")
                current_y_pos -= 1.5
            elif item_type == "heading":
                script_parts.append(f"        heading = Tex(r\"{content_clean}\", font_size=28).move_to(np.array([0, current_y_pos, 0]))")
                script_parts.append("        self.play(Write(heading))")
                script_parts.append("        elements_to_fade_out.add(heading)")
                script_parts.append("        self.wait(0.5)")
                current_y_pos -= 1
            elif item_type == "point" or item_type == "bullet" or item_type == "summary":
                prefix = "- " if item_type == "bullet" else ""
                script_parts.append(f"        point_text = Tex(r\"{prefix}{content_clean}\", font_size=22, tex_environment=\"{{minipage}}{{0.8\\linewidth}}\").move_to(np.array([0, current_y_pos, 0]))")
                script_parts.append("        self.play(FadeIn(point_text, shift=DOWN))")
                script_parts.append("        elements_to_fade_out.add(point_text)")
                script_parts.append("        self.wait(2)")
                current_y_pos -= (content_clean.count('\\\\n') + 1) * 0.5 + 0.3 # Adjust based on lines
            
            elif item_type == "image_placeholder":
                image_caption = item.get("caption", "Image").replace("'", "\\'").replace('"', '\\"').replace('\n', '\\\\n')
                original_url = item.get("image_url")
                
                if original_url and original_url in mock_local_image_paths:
                    img_local_path_str = str(mock_local_image_paths[original_url]).replace('\\', '/')
                    img_filename = Path(img_local_path_str).name
                    
                    script_parts.append(f"        # Displaying image: {image_caption}")
                    script_parts.append(f"        # Original URL: {original_url}")
                    script_parts.append(f"        # Expected local path for Manim: {img_local_path_str}")
                    script_parts.append(f"        # Ensure '{img_filename}' exists in assets_dir before running.")
                    script_parts.append("")
                    script_parts.append("        image_mobject = None")
                    script_parts.append("        image_group = VGroup()")
                    script_parts.append("        try:")
                    script_parts.append(f"            image_full_path = r\"{img_local_path_str}\"") # Use the full conceptual path directly
                    script_parts.append("            # In a real case, ensure this file exists due to prior download step.")
                    script_parts.append("            # For this script, Manim searches relative to where it runs or specified media_dir.")
                    script_parts.append("            # If not found, it will error. The assets_dir variable helps locate it.")
                    script_parts.append(f"            actual_image_file_to_load = os.path.join(assets_dir, \"{img_filename}\")")
                    script_parts.append("            if os.path.exists(actual_image_file_to_load):")
                    script_parts.append("                image_mobject = ImageMobject(actual_image_file_to_load).scale(0.6)")
                    script_parts.append("                image_mobject.move_to(np.array([0, current_y_pos - image_mobject.height/2, 0]))")
                    script_parts.append(f"                caption_obj = Tex(r\"{image_caption}\", font_size=18).next_to(image_mobject, DOWN, buff=0.2)")
                    script_parts.append("                image_group.add(image_mobject, caption_obj)")
                    script_parts.append("                self.play(FadeIn(image_group))")
                    script_parts.append("                elements_to_fade_out.add(image_group)")
                    script_parts.append("                self.wait(3)")
                    script_parts.append("                current_y_pos -= image_mobject.height + caption_obj.height + 0.5")
                    script_parts.append("            else:")
                    script_parts.append(f"                missing_img_text_str = \"Image not found: '{img_filename}'. Expected at \" + actual_image_file_to_load + \". Check assets_dir.\"")
                    script_parts.append(f"                missing_img_text = Tex(missing_img_text_str, font_size=18, color=YELLOW, tex_environment=\"{{minipage}}{{0.9\\linewidth}}\").move_to(np.array([0, current_y_pos - 0.5, 0]))")
                    script_parts.append("                self.play(Write(missing_img_text))")
                    script_parts.append("                elements_to_fade_out.add(missing_img_text)")
                    script_parts.append("                self.wait(2)")
                    script_parts.append("                current_y_pos -= 1.0")
                    script_parts.append("        except Exception as e:")
                    script_parts.append(f"            err_text_str = \"Error loading '{img_filename}': \" + str(e)[:100] + \".\"")
                    script_parts.append(f"            error_text = Tex(err_text_str, font_size=18, color=RED, tex_environment=\"{{minipage}}{{0.9\\linewidth}}\").move_to(np.array([0, current_y_pos - 0.5, 0]))")
                    script_parts.append("            self.play(Write(error_text))")
                    script_parts.append("            print(f\'Manim error loading image {img_local_path_str}: {e}\')") # For console debugging
                    script_parts.append("            elements_to_fade_out.add(error_text)")
                    script_parts.append("            self.wait(2)")
                    script_parts.append("            current_y_pos -= 1.0")
                else:
                    script_parts.append(f"        # Image URL {original_url} not mapped or no URL for placeholder.")
                    script_parts.append(f"        placeholder_text = Tex(r\"Image placeholder: {image_caption}\", font_size=18).move_to(np.array([0, current_y_pos - 0.5, 0]))")
                    script_parts.append("        self.play(Write(placeholder_text))")
                    script_parts.append("        elements_to_fade_out.add(placeholder_text)")
                    script_parts.append("        self.wait(1)")
                    current_y_pos -=1.0

            # Check if content is too low, then fade out and reset
            if current_y_pos < -3.5 and item_index < len(processed_data) - 1:
                script_parts.append("        self.play(FadeOut(elements_to_fade_out))")
                script_parts.append("        elements_to_fade_out = VGroup()") # Reset for next scene
                current_y_pos = 3.5
                script_parts.append("        self.wait(0.5)")


        script_parts.extend([
            "        if len(elements_to_fade_out) > 0:",
            "            self.play(FadeOut(elements_to_fade_out))",
            "        self.wait(1)",
            "",
            "# To run (ensure Manim is installed & images in assets_dir as specified):",
            "# 1. Create mock images in the assets_dir, e.g., ",
            f"#    {self.rag_assets_dir / Path('ai_investment.jpg').name}, {self.rag_assets_dir / Path('boeing_plane.jpg').name}, etc.",
            "# 2. Run: manim -pql your_script_name.py GeneratedExplainerScene"
        ])

        return "\\n".join(script_parts)

    def _sanitize_prompt(self, prompt: str) -> str:
        """Creates a safe filename base from a prompt."""
        return "".join(c if c.isalnum() else "_" for c in prompt)[:50].lower()

# Example of how it might be called (for testing, not part of the class)
# async def main():
#     service = RAGAnimationService()
#     prompt_example = "The impact of AI on renewable energy"
#     result_message = await service.generate_animation_from_prompt(prompt_example)
#     print(result_message)

# if __name__ == "__main__":
# import asyncio
# asyncio.run(main()) 