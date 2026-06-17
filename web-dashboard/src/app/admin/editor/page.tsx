"use client";

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Bold, Italic, Strikethrough, Code, Heading1, Heading2, List, ListOrdered } from 'lucide-react';

export default function EditorPage() {
  const editor = useEditor({
    extensions: [StarterKit],
    content: `
      <h1>The Next Generation of Proptech</h1>
      <p>Start writing your intelligence report here. The AIO bots will crawl this...</p>
    `,
    editorProps: {
      attributes: {
        class: 'prose prose-invert prose-sm sm:prose-base focus:outline-none max-w-full text-[#EDEDED] mt-8',
      },
    },
  });

  if (!editor) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <header>
        <h1 className="text-2xl font-semibold text-[#EDEDED] tracking-tight">AIO Editor</h1>
        <p className="text-sm text-[#888888] mt-1">Write intelligence reports directly into the database. JSON-LD is automatically injected.</p>
      </header>

      <div className="bg-[#111111] border border-[#222222] rounded-lg overflow-hidden min-h-[600px] flex flex-col">
        {/* Toolbar */}
        <div className="h-12 border-b border-[#222222] bg-[#161616] flex items-center px-4 gap-2 overflow-x-auto">
          <button 
            onClick={() => editor.chain().focus().toggleBold().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('bold') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Bold className="w-4 h-4" />
          </button>
          <button 
            onClick={() => editor.chain().focus().toggleItalic().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('italic') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Italic className="w-4 h-4" />
          </button>
          <button 
            onClick={() => editor.chain().focus().toggleStrike().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('strike') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Strikethrough className="w-4 h-4" />
          </button>
          <div className="w-px h-6 bg-[#333333] mx-1" />
          <button 
            onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('heading', { level: 1 }) ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Heading1 className="w-4 h-4" />
          </button>
          <button 
            onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('heading', { level: 2 }) ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Heading2 className="w-4 h-4" />
          </button>
          <div className="w-px h-6 bg-[#333333] mx-1" />
          <button 
            onClick={() => editor.chain().focus().toggleBulletList().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('bulletList') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <List className="w-4 h-4" />
          </button>
          <button 
            onClick={() => editor.chain().focus().toggleOrderedList().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('orderedList') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <ListOrdered className="w-4 h-4" />
          </button>
          <button 
            onClick={() => editor.chain().focus().toggleCodeBlock().run()} 
            className={`p-1.5 rounded hover:bg-[#2A2A2A] transition-colors ${editor.isActive('codeBlock') ? 'bg-[#2A2A2A] text-white' : 'text-[#888888]'}`}
          >
            <Code className="w-4 h-4" />
          </button>
        </div>

        {/* Editor Area */}
        <div className="flex-1 p-8 cursor-text">
          <EditorContent editor={editor} />
        </div>
      </div>
      
      <div className="flex justify-end">
        <button className="bg-white text-black px-6 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors">
          Publish Report
        </button>
      </div>
    </div>
  );
}
